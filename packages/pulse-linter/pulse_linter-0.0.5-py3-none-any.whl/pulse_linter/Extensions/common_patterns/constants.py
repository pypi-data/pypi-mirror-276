import ast
import re
from pulse_linter.Blacklist.build_1.blacklist import Blacklist_2
from pulse_linter.Blacklist.link_generator import LinkGen

class InsecurePatterns:
    name = 'flake8_security_checker'
    version = '0.0.1'

    def __init__(self, tree):
        self.tree = tree
        self.patterns = Blacklist_2.gen_blacklist()

    def patterns_inlist(self):
        compiled_patterns = []
        for pattern_dict in self.patterns:
            for pattern in pattern_dict['qualname']:
                compiled_patterns.append((pattern_dict['bid'], pattern_dict['message'], re.compile(pattern, re.IGNORECASE)))
        return compiled_patterns

    def pattern_matcher(self):
        for pattern_id, message, pattern in self.patterns_inlist():
            try:
                for node in ast.walk(self.tree):
                    if isinstance(node, ast.Constant) and isinstance(node.value, str):
                        if pattern.search(node.value):
                            yield (
                                node.lineno,
                                node.col_offset,
                                f'SC102 Matched against bad re:{pattern} - {message} \nfor more information visit {LinkGen(pattern_id).link()}',
                                type(self)
                            )

            except re.error as e:
                print(f"Error compiling pattern '{pattern.pattern}': {e}")

    def run(self):
        return self.pattern_matcher()


