import ast

class SecurityChecker:
    name = 'flake8_security_checker'
    version = '0.0.1'

    def __init__(self, tree):
        self.tree = tree

    def use_eval(self, node):
        if isinstance(node.func, ast.Name) and node.func.id == 'eval':
            return True
        return False

    def run(self):
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Call):
                if self.use_eval(node):
                    yield (
                        node.lineno,
                        node.col_offset,
                        'SC101: Potential use of eval may cause security issues',
                        type(self),
                    )
