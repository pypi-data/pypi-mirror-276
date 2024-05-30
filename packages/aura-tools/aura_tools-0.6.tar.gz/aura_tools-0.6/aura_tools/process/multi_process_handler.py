from multiprocessing import Process

from aura_tools.code_explanation_generator import CodeExplanationGenerator


class MultiProcessHandler:
    def __init__(self, data, process_func, num_processes=None, **kwargs):
        self.data = data
        self.process_func = process_func
        self.num_processes = num_processes or len(data)
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


def process_files(api_key, secret_key, data_chunk, process_id, **kwargs):
    generator = CodeExplanationGenerator(api_key, secret_key,
                                         result_file=f"outputs/result{process_id}.json",
                                         error_file=f"outputs/error{process_id}.json")
    generator.process_files(data_chunk)


if __name__ == '__main__':
    api_key = ""
    secret_key = ""

    java_files = CodeExplanationGenerator(api_key, secret_key).download_and_scan(
        'https://github.com/langchain4j/langchain4j')

    handler = MultiProcessHandler(data=java_files,
                                  process_func=process_files,
                                  num_processes=6,
                                  api_key=api_key,
                                  secret_key=secret_key)
    handler.run()
