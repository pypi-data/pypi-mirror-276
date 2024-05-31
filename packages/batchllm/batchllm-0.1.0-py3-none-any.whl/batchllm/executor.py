#!/usr/bin/python
import os
import json
from absl import app
from absl import flags
from absl import logging
from odps import ODPS
from odps.tunnel import TableTunnel
from vllm import LLM, SamplingParams
from modelscope import snapshot_download

FLAGS = flags.FLAGS

# template
#flags.DEFINE_integer('age', None, 'Your age in years.', lower_bound=0) 
#flags.DEFINE_float("weight", None, "Your weight in kg.", lower_bound=0)
#flags.DEFINE_boolean('debug', False, 'Produces debugging output.')
#flags.DEFINE_enum('job', 'running', ['running', 'stopped'], 'Job status.') #DEFINE_enum()函数()中各元素分别代表name,default,enum_values,help
#flags.DEFINE_list("food", None, "Your favorite food")

# user config
flags.DEFINE_string('infer_kernel', 'SingleInfer', 'user define class for infer.') 

# odps config
flags.DEFINE_string('access_id', '', 'odps access id.') 
flags.DEFINE_string('access_key', '', 'odps access key.') 
flags.DEFINE_string('project', 'bi_strategy', 'odps project.') 
flags.DEFINE_string('endpoint', 'http://service-corp.odps.aliyun-inc.com/api', 'odps endpoint.') 

# table config
flags.DEFINE_string('input_table', '', 'Input table name.') 
flags.DEFINE_string('input_partition', '', 'Input table partition name.') 
flags.DEFINE_string('column', 'prompts', 'Input table column.') 
flags.DEFINE_string('output_table', '', 'Output table name.') 
flags.DEFINE_string('output_partition', '', 'Output table partition name.') 

# LLM init config
flags.DEFINE_string('model_name', '', 'model name.') 
flags.DEFINE_boolean('enable_prefix_caching', False, 'enable prefix caching.') 

# sampling config
flags.DEFINE_integer('max_tokens', 500, 'max tokens.') 
flags.DEFINE_integer("top_k", -1, "the numbers of top tokens")
flags.DEFINE_float("top_p", 1.0, "control the cumulative prob.", lower_bound=0)


def check_config():
    if not all((FLAGS.access_id, FLAGS.access_key, FLAGS.input_table, FLAGS.input_partition)):
        logging.error(f"access_id、access_key、input_table、input_partition is null")
    if not FLAGS.output_table:
        FLAGS.output_table = FLAGS.input_table
    if not FLAGS.output_partition:
        FLAGS.output_partition = FLAGS.input_partition + "_llm_infer"
    if not FLAGS.model_name:
        FLAGS.model_name = 'qwen/Qwen1.5-7B-Chat-AWQ'
    if FLAGS.infer_kernel not in InferFactory.factory_registry:
        logging.error(f'User deinfed kernel {FLAGS.infer_kernel} not be register')
    logging.info(f"flags: {json.dumps(FLAGS.flag_values_dict(), indent=4)}")


# default kernel
class SingleInfer:
 
    def compute(self, ctx):
        return ctx.llm(ctx.batch)

    def warm_up(self, llm):
        pass


class InferFactory:
    factory_registry = {
        'SingleInfer' : SingleInfer
    }
    
    @classmethod
    def register(cls, infer_class):
        cls.factory_registry[infer_class.__name__] = infer_class

    @classmethod
    def get_kernel(cls, name):
        return cls.factory_registry[name]


class InferContext:

    def __init__(self, llm, batch):
        self.llm = llm
        self.batch = batch


class OdpsHandle:

    def __init__(self, access_id, access_key, project, endpoint, input_table, input_partition, column, output_table, output_partition):

        self.column = column
        odps = ODPS(access_id, access_key, project, endpoint=endpoint)

        self.worker_num = int(os.environ.get("WORKER_SIZE", "1"))
        self.index = int(os.environ.get("RANK", "0"))

        download_session = TableTunnel(odps).create_download_session(input_table, partition_spec=input_partition)
        data_size = download_session.count//self.worker_num
        if self.index == self.worker_num-1:
            count = download_session.count - (self.worker_num-1)*data_size
        else:
            count = data_size
        start = self.index*data_size
        self.reader = download_session.open_arrow_reader(start, count, columns=[column])

        if self.worker_num == 1:
            partition_spec = output_partition
        else:
            partition_spec = output_partition + "_" + str(self.index)
        self.table = odps.get_table(output_table)
        self.table.create_partition(partition_spec, if_not_exists=True) 
        upload_session = TableTunnel(odps).create_stream_upload_session(output_table, partition_spec=partition_spec)
        self.writer = upload_session.open_record_writer()
        
        logging.info(f"Odps init info: {locals()}")

    def __enter__(self):
        return self

    def __exit__(self, type, value, trace):
        self.reader.close()
        self.writer.close()

    def batch(self):
        return self.reader.read()[self.column].to_pylist()

    def write(self, batch_results):
        for q, a in zip(batch_results["prompts"], batch_results["generated_text"]):
            record = self.table.new_record()
            record['prompts'] = q
            record['generated_text'] = a
            self.writer.write(record)


class LLMPredictor:

    def __init__(self, model_path,
                 enable_prefix_caching=False,
                 max_tokens=None,
                 top_p=None,
                 top_k=None):
        tensor_parallel_size = int(os.environ.get("NPROC_PER_NODE", "1"))
        self.llm = LLM(model=model_path,
                       enable_prefix_caching=enable_prefix_caching,
                       tensor_parallel_size=tensor_parallel_size)

        self.sampling_params = SamplingParams(max_tokens=max_tokens,
                                              top_p=top_p,
                                              top_k=top_k,)

        logging.info("LLMPredictor init done!")

    def __call__(self, batch):
        outputs = self.llm.generate(batch, self.sampling_params)
        prompt = []
        generated_text = []
        for output in outputs:
            prompt.append(output.prompt)
            generated_text.append(' '.join([o.text for o in output.outputs]))
        return {
            "prompts": prompt,
            "generated_text": generated_text,
        }


class Executor:

    def __init__(self):

        check_config()
    
        model_dir = snapshot_download(FLAGS.model_name)
    
        self.llm_predictor = LLMPredictor(model_dir,
                                          FLAGS.enable_prefix_caching,
                                          FLAGS.max_tokens,
                                          FLAGS.top_p,
                                          FLAGS.top_k)

        self.kernel = InferFactory.get_kernel(FLAGS.infer_kernel)()

        logging.info(f"Executor kernel: {FLAGS.infer_kernel}")

    def run(self):
        
        if hasattr(self.kernel, 'warm_up'):
            logging.info(f"Warm Up: {json.dumps(self.kernel.warm_up(self.llm_predictor), indent=4, ensure_ascii=False)}")

        with OdpsHandle(FLAGS.access_id,
                        FLAGS.access_key,
                        FLAGS.project,
                        FLAGS.endpoint,
                        FLAGS.input_table,
                        FLAGS.input_partition,
                        FLAGS.column,
                        FLAGS.output_table,
                        FLAGS.output_partition) as handle:
            counter = 0
            while True:
                batch = handle.batch()
                if batch==[]: break
                outputs = self.kernel.compute(InferContext(self.llm_predictor, batch))
                handle.write(outputs)
                if counter % 1 == 0:
                    logging.info(f"Process batch: {counter}, size: {len(batch)}")
                counter += 1


def infer_main(argv):
    Executor().run()


if __name__ == '__main__':  
    logging.get_absl_handler().setLevel(logging.INFO)
    app.run(infer_main)
