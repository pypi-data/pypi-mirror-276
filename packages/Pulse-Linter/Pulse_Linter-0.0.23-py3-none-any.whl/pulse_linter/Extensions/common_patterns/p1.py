import ast
import re
from pulse_linter.Blacklist.build_1 import constants as c


class BlacklistCheckerError(Exception):
    pass

class BlacklistChecker:
    name = 'flake8_security_checker'
    version = '0.0.1'

    def __init__(self, tree, filename='(none)'):
        self.tree = tree
        self.filename = filename
        self.blist = c.blist
        self._compiled_regexes = {}  # Cache for compiled regexes

    def run(self):
        for item in self.blist:
            for qualname in item['qualname']:
                pattern = qualname.replace('(?i)', '')
                try:
                    if pattern not in self._compiled_regexes:
                        self._compiled_regexes[pattern] = re.compile(f'(?i){pattern}', re.IGNORECASE)
                    regex = self._compiled_regexes[pattern]
                    for node in ast.walk(self.tree):
                        if isinstance(node, ast.Call):
                            if isinstance(node.func, ast.Attribute):
                                node_qual = f'{node.func.value.id}.{node.func.attr}'
                            else:
                                node_qual = node.func.id
                            if regex.fullmatch(node_qual):
                                yield (
                                    node.lineno,
                                    node.col_offset,
                                    f"{item['level']}: {item['message']} (CWE-{item['cwe']}, BID-{item['bid']})",
                                    type(self)
                                )
                except re.error as e:
                    raise BlacklistCheckerError(f"Regex error for pattern {qualname}: {e}")

# Flake8 extension hook
def get_plugin_class():
    return BlacklistChecker

# Example usage for standalone testing (not needed for Flake8 integration)
if __name__ == "__main__":
    code = """
import os
os.system('ls')
subprocess.Popen(['ls', '-l'])
eval('2 + 2')
exec('print("Hello, World!")')
"""

    tree = ast.parse(code)
    checker = BlacklistChecker(tree)
    for warning in checker.run():
        print(warning)
