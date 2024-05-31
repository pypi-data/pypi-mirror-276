import threading

from aura_tools.code_explanation_generator import CodeExplanationGenerator
from aura_tools.llm.tongyi_ai_client import TongYiQianWenClient


class MultiThreadHandler:
    def __init__(self, data, process_func, num_threads=None, **kwargs):
        self.data = data
        self.process_func = process_func
        self.num_threads = num_threads or 1
        self.kwargs = kwargs

    def split_into_chunks(self):
        chunk_size = len(self.data) // self.num_threads
        chunks = [self.data[i * chunk_size: (i + 1) * chunk_size] for i in range(self.num_threads)]

        if len(self.data) % self.num_threads != 0:
            chunks[-1].extend(self.data[self.num_threads * chunk_size:])

        return chunks

    def process_chunk(self, chunk, thread_id):
        kwargs = self.kwargs.copy()
        kwargs['data_chunk'] = chunk
        kwargs['thread_id'] = thread_id
        self.process_func(**kwargs)

    def run(self):
        threads = []
        chunks = self.split_into_chunks()

        for i, chunk in enumerate(chunks):
            t = threading.Thread(target=self.process_chunk, args=(chunk, i))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()


def process_files(data_chunk, thread_id, client, description="", prompt="", **kwargs):
    generator = CodeExplanationGenerator(client=client,
                                         result_file=f"outputs/result{thread_id}.json",
                                         error_file=f"outputs/error{thread_id}.json",
                                         description=description,
                                         prompt=prompt)
    generator.process_files(data_chunk)


if __name__ == '__main__':
    # 千问
    api_key = ""
    client = TongYiQianWenClient(api_key, model="qwen-long")

    generator = CodeExplanationGenerator(client=client, description="这是一个关于langchain的Java版本项目源码")
    java_files = generator.download_and_scan('https://github.com/langchain4j/langchain4j')

    prompt = ""

    handler = MultiThreadHandler(data=java_files,
                                 process_func=process_files,
                                 num_threads=2,  # 设置线程数
                                 client=client,
                                 description="这是langchain的一个Java版本项目源码",
                                 prompt=prompt)
    handler.run()

