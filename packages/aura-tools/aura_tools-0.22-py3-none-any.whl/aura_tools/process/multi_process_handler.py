from multiprocessing import Process

from aura_tools.code_explanation_generator import CodeExplanationGenerator


class MultiProcessHandler:
    def __init__(self, data, process_func, num_processes=None, **kwargs):
        self.data = data
        self.process_func = process_func
        self.num_processes = num_processes or 1
        self.kwargs = kwargs

    def split_into_chunks(self):
        chunk_size = len(self.data) // self.num_processes
        chunks = [self.data[i * chunk_size: (i + 1) * chunk_size] for i in range(self.num_processes)]

        if len(self.data) % self.num_processes != 0:
            chunks[-1].extend(self.data[self.num_processes * chunk_size:])

        return chunks

    def process_chunk(self, chunk, process_id):
        kwargs = self.kwargs.copy()
        kwargs['data_chunk'] = chunk
        kwargs['process_id'] = process_id
        self.process_func(**kwargs)

    def run(self):
        processes = []
        chunks = self.split_into_chunks()

        for i, chunk in enumerate(chunks):
            p = Process(target=self.process_chunk, args=(chunk, i))
            processes.append(p)
            p.start()

        for p in processes:
            p.join()


# ① [注意：目前这个启动函数，貌似需要定义在这里，不能跟启动的__main__在一个文件中]
# 这个启动函数定义，应该每个任务自己进行定义，此处起到示例的作用
def process_files(data_chunk, process_id, client, description="", prompt="", **kwargs):
    generator = CodeExplanationGenerator(client=client,
                                         result_file=f"outputs/result{process_id}.json",
                                         error_file=f"outputs/error{process_id}.json",
                                         description=description,
                                         prompt=prompt)
    generator.process_files(data_chunk)


# ② 需要在其他模块才能执行这个代码，否则多进程会有问题
# if __name__ == '__main__':
#     from multi_process_handler import MultiProcessHandler, process_files
#     from aura_tools.llm.baidu_ai_client import BaiduAIClient
#     from aura_tools.code_explanation_generator import CodeExplanationGenerator
#
#     api_key = ""
#     secret_key = ""
#     client = BaiduAIClient(f"{api_key}|{secret_key}")
#
#     generator = CodeExplanationGenerator(client=client, description="这是一个关于langchain的Java版本项目源码")
#     java_files = generator.download_and_scan('https://github.com/langchain4j/langchain4j')
#
#     handler = MultiProcessHandler(data=java_files,
#                                   process_func=process_files,
#                                   num_processes=1,
#                                   client=client,
#                                   description="",
#                                   prompt="")
#     handler.run()
