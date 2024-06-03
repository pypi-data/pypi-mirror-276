import ast
from pulse_linter.Blacklist.imports.blacklist import Blacklist
from pulse_linter.Blacklist.link_generator import LinkGen

class BadImportfrom:
    name = 'flake8_security_checker'
    version = '0.0.1'

    def __init__(self, tree):
        self.tree = tree
        self.blist = Blacklist.gen_blacklist()

    def all_qualnames(self):
        for each_dict in self.blist:
            for node in ast.walk(self.tree):
                if isinstance(node, ast.ImportFrom):
                    imported_name = f'{node.module}.{node.names[0].name}'
                    if imported_name in each_dict['qualname']:
                        yield (
                            node.lineno,
                            node.col_offset,
                            f"SC104 Use of bad from and import {imported_name} {each_dict['message']}\nfor more information\t{LinkGen(each_dict['bid']).link()}",
                            type(self)
                        )
    def run(self):
        return self.all_qualnames()

# files = open(r'C:\Users\bornd\PycharmProjects\Flake_extension\test.py','r')
# b = BadImportfrom(ast.parse(files.read()))
# print(b.all_qualnames())