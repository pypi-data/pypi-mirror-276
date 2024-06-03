import ast
import re

class SnakeCaseChecker:
    name = 'flake8_snake_case_checker'
    version = '0.0.1'
    pattern = re.compile(r'^[a-z_][a-z0-9_]*$')

    def __init__(self, tree):
        self.tree = tree

    def run(self):
        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef):
                if not self.pattern.match(node.name):
                    yield (
                        node.lineno,
                        node.col_offset,
                        f'NC101 Function name "{node.name}" is not snake_case',
                        type(self),
                    )
