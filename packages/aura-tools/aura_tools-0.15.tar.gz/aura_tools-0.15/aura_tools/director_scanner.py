"""
① 先扫描所有文件，然后按类型分类
② 让大模型看哪些是有价值的类型，然后再过滤第二遍，找到代码文件和文档文件合成大文本文件扔给大模型执行任务。
"""

import os
from typing import List, Dict, Optional


class DirectoryScanner:
    def __init__(self, directory: str, filter_types: Optional[List[str]] = None):
        self.directory = directory
        self.filter_types = filter_types or self.get_default_filter_types()

    """① 扫描目录获得所有文件列表"""

    def scan_all(self) -> List[str]:
        all_files = [os.path.join(root, file) for root, dirs, files in os.walk(self.directory) for file in files]
        print(f"Total files: {len(all_files)}")
        return all_files

    @staticmethod
    def get_file_type(file: str) -> str:
        return os.path.splitext(file)[1]

    def count_file_types(self, files: List[str]) -> Dict[str, int]:
        file_types = {}
        for file in files:
            file_type = self.get_file_type(file)
            file_types[file_type] = file_types.get(file_type, 0) + 1
        return file_types

    @staticmethod
    def sort_file_types(file_types: Dict[str, int]) -> Dict[str, int]:
        return dict(sorted(file_types.items(), key=lambda item: item[1], reverse=True))

    """② 获取目标文件类型列表(可以通过大模型筛选出目标文件列表)"""

    @staticmethod
    def get_default_filter_types() -> List[str]:
        return [".py", ".ipynb", ".mdx", ".md", ".sh", ".yml", ".yaml", ".txt", ".rst"]

    """③ 过滤文件列表"""

    def filter_files_by_type(self, files: List[str]) -> List[str]:
        return [file for file in files if self.get_file_type(file) in self.filter_types]


"""[TODO] : 大模型过滤出目标文件类型 ① scan_all ② count_file_types ③ llm_select_type"""

if __name__ == "__main__":
    # scanner = DirectoryScanner(r"langchain4j")
    custom_filter_types = [".java"]
    scanner = DirectoryScanner(r"langchain4j", filter_types=custom_filter_types)

    all_files = scanner.scan_all()
    filtered_files = scanner.filter_files_by_type(all_files)
    file_types_count = scanner.count_file_types(filtered_files)
    sorted_file_types = scanner.sort_file_types(file_types_count)
    print(sorted_file_types)
    print(scanner.sort_file_types(scanner.count_file_types(all_files)))
