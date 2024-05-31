import json


def replace_path_prefix(original_path, new_prefix=None, find_str=None):
    if find_str is None or new_prefix is None:
        return original_path;
    # 找到 find_str 在路径中的索引
    index_find = original_path.find(find_str)

    # 如果 find_str 存在于路径中，则替换之前的部分
    if index_find != -1:
        # 替换 find_str 之前的部分
        return new_prefix + original_path[index_find:]
    else:
        # 如果 find_str 不存在，则返回原路径
        return original_path


def filter_error_data(json_list):
    return [json for json in json_list if json["function_explanation"] is not None and "error_code" not in json["function_explanation"]];


def escape_comment(comment):
    """转义注释中的特殊字符"""
    return comment.replace('*/', '*\\/')


class CommentInserter:
    def __init__(self, result_file='outputs/result.json', new_prefix=None, find_str=None):
        self.result_file = result_file
        self.new_prefix = new_prefix
        self.find_str = find_str

    def load_generated_comments(self):
        """加载生成的注释数据"""
        with open(self.result_file, 'r', encoding='utf-8') as file:
            data = [json.loads(line) for line in file]
        return data

    # 过滤掉不符合条件的数据

    def insert_comments(self, data):
        """将注释插入到对应的Java源文件中"""
        for item in data:
            code_file = replace_path_prefix(item['code_file'], self.new_prefix, self.find_str)
            function_source = item['function_source']
            try:
                function_explanation = escape_comment(item['function_explanation'])
            except KeyError:
                print(f"未找到函数: {function_source} in {code_file}")

            # 读取Java源文件内容
            with open(code_file, 'r', encoding='utf-8') as file:
                content = file.read()

            # 查找函数位置
            func_index = content.find(function_source)
            if func_index != -1:
                # 插入注释
                comment = f"/**\n * {function_explanation}\n */\n"
                new_content = content[:func_index] + comment + content[func_index:]

                # 写回文件
                with open(code_file, 'w', encoding='utf-8') as file:
                    file.write(new_content)
                print(f"注释已插入文件: {code_file}")
            else:
                print(f"未找到函数: {function_source} in {code_file}")

    def run(self):
        """运行注释插入流程"""
        data = self.load_generated_comments()
        self.insert_comments(data)


if __name__ == '__main__':
    inserter = CommentInserter(result_file="result.json")
    inserter.run()
