import json
from datetime import datetime

from aura_tools.director_scanner import DirectoryScanner

from aura_tools.github_repository_downloader import GithubRepositoryDownloader
from aura_tools.java_function_extractor import JavaFunctionExtractor
from aura_tools.json_file_util import JsonFileUtils
from aura_tools.llm.baidu_ai_client import BaiduAIClient


class CodeExplanationGenerator:
    def __init__(self, client, result_file='outputs/result.json', error_file='outputs/error.json', description="", prefix="", prompt="", suffix="" ):
        self.client = client
        self.result_file = JsonFileUtils(result_file)
        self.error_file = JsonFileUtils(error_file)
        self.explanation_functions = self._load_existing_explanations()
        self.description = description
        self.prefix = prefix
        self.prompt = prompt;
        self.suffix = suffix

    def _load_existing_explanations(self):
        """加载已有的解释函数,避免重复解读"""
        json_data = self.result_file.load_json_lines()
        return [item['function_source'] for item in json_data]

    def _check_is_exist(self, function_source):
        """检查函数是否已经解读过"""
        return any(function_source.strip() == func.strip() for func in self.explanation_functions)

    def _llm_explanation_function(self, code, prefix="", suffix="", prompt=""):
        """使用大模型解释函数代码"""
        messages = [
            {
                "role": "user",
                "content": f"{prefix}\n{prompt}\n{code}\n{suffix}"
            }
        ]
        try:
            print(messages)
            result = self.client.send_request(messages)
            result = self.client.parse_result(result);
            print(result)
            return result
        except Exception as e:
            print(f"请求失败:{str(e)}")
            raise Exception(f"Request failed after {self.client.max_retries} retries: {str(e)}")

    def _process_file(self, file):
        """处理单个Java文件,提取函数并解读"""
        try:
            extractor = JavaFunctionExtractor(file)
            functions = extractor.extract_functions()
            total_func = len(functions)
            # 逐个函数解读
            for func_index, (func_name, func_code) in enumerate(functions):
                print(f"正在处理函数: 第 {func_index + 1} 个函数，共 {total_func} 个函数, func_name = {func_name}, \nfunc_code = {func_code}\n")
                if self._check_is_exist(func_code):
                    print(f"已经处理过这段代码 : file={file},func_name={func_name},func_code={func_code}")
                    continue
                prefix = self.prefix if self.prefix else f"这段函数来自于{file}"
                if self.description:
                    prefix = f"{prefix}; \n项目的基本信息描述是:{self.description}\n"
                prompt = self.prompt if self.prompt else "请分析输出这段代码的含义,并为它添加详细的注释说明:"
                explanation = self._llm_explanation_function(func_code, prefix=prefix, prompt=prompt, suffix=self.suffix)
                result = {
                    "code_file": file,
                    "function_source": func_code,
                    "function_explanation": explanation
                }
                print(result)
                self.result_file.append_json_line(json.dumps(result, ensure_ascii=False))
        except Exception as e:
            print(f"Error: {e}")
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.error_file.append_json_line(f"{timestamp} Error: {e} , file = {file}")

    @staticmethod
    def download_and_scan(repo_url,target_dir='.'):
        """下载仓库并扫描Java文件"""
        dir_path = GithubRepositoryDownloader(repo_url=repo_url,target_dir=target_dir).download()
        print(f"仓库已下载到: {dir_path}")

        scanner = DirectoryScanner(dir_path, filter_types=['.java'])
        all_files = scanner.scan_all()
        java_files = scanner.filter_files_by_type(all_files)
        return java_files

    def process_files(self, files_list):
        """处理文件列表"""
        file_total = len(files_list)
        for file_index, file in enumerate(files_list):
            print(f"正在处理第 {file_index + 1} 个文件,共 {file_total} 个文件 , file = {file}")
            self._process_file(file)

    def run(self, repo_url,target_dir='.'):
        """运行代码解释生成流程"""
        java_files = self.download_and_scan(repo_url=repo_url,target_dir=target_dir)
        self.process_files(java_files)

if __name__ == '__main__':
    # 百度
    api_key = ""
    secret_key = ""
    client = BaiduAIClient(f"{api_key}|{secret_key}");

    generator = CodeExplanationGenerator(client=client,description="这是一个关于langchain的Java版本项目源码")
    # java_files = generator.download_and_scan('https://github.com/langchain4j/langchain4j')

    # 单进程模式
    generator.run('https://github.com/langchain4j/langchain4j')