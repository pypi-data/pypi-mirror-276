import ast
from pulse_linter.Blacklist.imports.blacklist import Blacklist
from pulse_linter.Blacklist.link_generator import LinkGen

class BadImports:
    name = 'flake8_security_checker'
    version = '0.0.1'

    def __init__(self, tree):
        self.tree = tree
        self.blist = Blacklist.gen_blacklist()

    def all_qualnames(self):
        for each_dict in self.blist:
            for node in ast.walk(self.tree):
                if isinstance(node, ast.Import):
                    for name in node.names:
                        imported_name = name.name
                        if imported_name in each_dict['qualname']:
                            yield (
                                node.lineno,
                                node.col_offset,
                                f"SC103  1  Use of bad imports {imported_name} {each_dict['message']}\nfor more information\t{LinkGen(each_dict['bid']).link()}",
                                type(self)
                            )

    def run(self):
        return self.all_qualnames()

# files = open(r'C:\Users\bornd\PycharmProjects\Flake_extension\test.py','r')
# b = BadImports(ast.parse(files.read()))
# print(b.all_qualnames())