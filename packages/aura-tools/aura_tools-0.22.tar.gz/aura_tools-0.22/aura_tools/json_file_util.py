"""
工具类：
① 支持向文本文件中按行追加json，需要支持传入一个json字符串，就在文件中写入追加一行
② 支持加载文本文件，将每一行转换为json，然后读取文件为一个json列表
"""

import json
import os


class JsonFileUtils:
    def __init__(self, file_path):
        self.file_path = file_path

    def append_json_line(self, json_str):
        """
        将一个JSON字符串追加写入文件的新行
        :param json_str: JSON字符串
        """

        # 获取文件夹路径，如果没有文件夹路径则返回空字符串
        dir_path = os.path.dirname(self.file_path)

        # 如果 dir_path 为空字符串，说明文件在当前目录
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path)

        # 然后执行写入操作
        with open(self.file_path, 'a', encoding='utf-8') as file:
            file.write(json_str + '\n')
            file.flush()  # 立即将缓冲区内容写入磁盘

    def load_json_lines(self):
        """
        加载文件中的JSON数据,每行作为一个JSON对象,返回JSON对象列表
        :return: JSON对象列表
        """
        json_list = []
        if not os.path.exists(self.file_path):
            return json_list
        with open(self.file_path, 'r', encoding='utf-8') as file:
            for line in file:
                json_obj = json.loads(line.strip())
                json_list.append(json_obj)
        return json_list


if __name__ == '__main__':
    # 创建 JsonFileUtils 实例
    utils = JsonFileUtils('data.json')

    # 追加JSON字符串到文件
    utils.append_json_line('{"name": "John", "age": 30}')
    utils.append_json_line('{"name": "Alice", "age": 25}')

    # 从文件加载JSON数据
    json_data = utils.load_json_lines()
    print("Loaded JSON data:")
    for item in json_data:
        print(item)

    # 追加更多的JSON字符串到文件
    utils.append_json_line('{"name": "Bob", "age": 35}')
    utils.append_json_line('{"name": "Emma", "age": 28}')

    # 再次从文件加载JSON数据
    json_data = utils.load_json_lines()
    print("\nUpdated JSON data:")
    for item in json_data:
        print(item)
