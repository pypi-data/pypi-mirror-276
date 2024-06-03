import ast


class EvalChecker:
    def __init__(self, tree):
        self.tree = tree
        self.result = []
    def checker_function(self):
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name) and node.func.id == 'eval':
                    # print("1 Found eval call at line", node.lineno)
                    yield (
                        node.lineno,
                        node.col_offset,
                        f"SM101 Usage of eval for more information {'https://cwe.mitre.org/data/definitions/95.html'}",
                        type(self)
                    )
                elif isinstance(node.func, ast.Attribute) and node.func.attr == 'eval':
                    # print("2 Found eval call at line", node.lineno)
                    yield (
                        node.lineno,
                        node.col_offset,
                        f"SM101 Usage of eval for more information {'https://cwe.mitre.org/data/definitions/95.html'}",
                        type(self)
                    )
    def run(self):
        return self.checker_function()



# files = open(r"C:\Users\bornd\PycharmProjects\Flake_extension\test.py",'r')
# b = EvalChecker(ast.parse(files.read()))
#
# print(b.run())