"""
临时处理之前不完整导致的代码source段
"""
from aura_tools.director_scanner import DirectoryScanner
from aura_tools.github_repository_downloader import GithubRepositoryDownloader
from aura_tools.java_function_extractor import JavaFunctionExtractor

def new_extract_functions(java_files):
    # 接收所有函数
    all_functions = []
    # 读取目标文件函数
    for i, file in enumerate(java_files):
        print(f"file -> index : {i}")
        try:
            functions = JavaFunctionExtractor(file).extract_functions()
            for func in functions:
                new_function_source = func[1];
                all_functions.append(
                    {
                        "code_file": file,
                        "new_function_source": new_function_source,
                    }
                )
            print(len(all_functions))
        except Exception as e:
            print(e)
    return all_functions;


# 统计有多少个函数需要解释说明
if __name__ == '__main__':
    # dir_path = r'project_source_dir';
    # 下载仓库到本地
    dir_path = GithubRepositoryDownloader('https://github.com/google/volley.git').download()
    print(dir_path)

    # 扫描目标文件
    scanner = DirectoryScanner(dir_path,filter_types=['.java'])
    all_files = scanner.scan_all()
    java_files = scanner.filter_files_by_type(all_files)

    # 提取新函数
    new_all_functions = new_extract_functions(java_files)
    print(len(new_all_functions))
