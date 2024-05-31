import javalang

class JavaFunctionExtractor:

    def __init__(self, java_file):
        self.java_file = java_file

    def extract_functions(self):
        functions = []
        with open(self.java_file, 'r', encoding='utf-8') as file:
            java_code = file.read()
            tree = javalang.parse.parse(java_code)
            for path, node in tree.filter(javalang.tree.MethodDeclaration):
                func_name = node.name
                return_type = node.return_type.name if node.return_type else 'void'
                func_code = self._extract_function_code(java_code, node)  # Pass the node instead of start_line
                functions.append((func_name, func_code))
        return functions

    def _extract_function_code(self, java_code, node):
        lines = java_code.split('\n')
        start_line = node.position.line - 1

        func_lines = []

        # Start looking for annotations and function signature from the start line
        for i in range(start_line - 1, -1, -1):
            line = lines[i].strip()
            if line.startswith("@"):
                func_lines.insert(0, lines[i])
            else:
                break

        # Capture the function body
        bracket_count = 0
        end_line = start_line
        for i in range(start_line, len(lines)):
            line = lines[i]
            func_lines.append(line)
            bracket_count += line.count('{')
            bracket_count -= line.count('}')
            if bracket_count == 0:
                end_line = i
                break

        return '\n'.join(func_lines)

def main():
    java_file = r'Test.java'
    extractor = JavaFunctionExtractor(java_file)
    functions = extractor.extract_functions()
    for func_name, func_code in functions:
        print(f"Function Name: {func_name}")
        print(f"Function Code:\n{func_code}\n")

if __name__ == '__main__':
    main()
