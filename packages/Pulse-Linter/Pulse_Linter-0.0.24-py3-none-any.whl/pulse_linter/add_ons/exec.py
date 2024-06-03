import ast

class ExecChecker:
    def __init__(self,tree):
        self.tree = tree

    def use_of_exec(self):
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                if node.func.id == 'exec':
                    yield (
                        node.lineno,
                        node.col_offset,
                        f"SM102 Use of eval {'https://www.guvi.in/blog/why-is-using-eval-a-bad-practice/'}",
                        type(self)
                    )
    def run(self):
        return self.use_of_exec()


# file = open(r'C:\Users\bornd\PycharmProjects\Tree Analysis\test.py','r')
# content = file.read()
# j = ExecChecker(ast.parse(content))
# j.use_of_exec()


