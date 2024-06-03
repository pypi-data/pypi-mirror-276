import ast
import re
from pulse_linter.Blacklist.imports.blacklist import Blacklist
from pulse_linter.Blacklist.link_generator import LinkGen

class BadAttributes:
    name = 'flake8_security_checker'
    version = '0.0.1'

    def __init__(self, tree, filename):
        self.tree = tree
        self.filename = filename
        self.attributes = Blacklist.gen_blacklist()
        self.errors = []

    def patterns_inlist(self):
        compiled_patterns = []
        for pattern_dict in self.attributes:
            for pattern in pattern_dict['qualname']:
                compiled_patterns.append(
                    (pattern_dict['bid'], pattern_dict['message'], re.compile(pattern, re.IGNORECASE)))
        return compiled_patterns

    def pattern_matcher(self):
        for pattern_id, message, pattern in self.patterns_inlist():
            try:
                for node in ast.walk(self.tree):
                    if isinstance(node, ast.Call):
                        if isinstance(node.func, ast.Attribute):
                            if pattern.match(node.func.attr) or pattern.match(node.func.value.id):
                                base_name = node.func.value.id
                                attr_name = node.func.attr
                                self.errors.append((
                                    node.lineno,
                                    node.col_offset,
                                    f'SC105 Use of blacklisted attributes : {base_name}.{attr_name} - {message}\nfor more information visit\t{LinkGen(pattern_id).link()}',
                                    type(self)
                                ))
                        elif isinstance(node.func, ast.Name):
                            if pattern.match(node.func.id):
                                base_name = node.func.id
                                self.errors.append((
                                    node.lineno,
                                    node.col_offset,
                                    f'SC104 {pattern_id}: {message} - {base_name}',
                                    type(self)
                                ))
            except Exception as e:
                print(f"Error processing pattern {pattern_id}: {e}")

    def run(self):
        self.pattern_matcher()
        for error in self.errors:
            yield error
