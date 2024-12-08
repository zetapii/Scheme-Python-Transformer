import ast
import astunparse
from racket_to_python import racket_ast_to_python_ast
from parsers import tokenize_racket

class RacketTransformer(ast.NodeTransformer):
    """
    Transforms racket_insert calls by replacing them
    with their Python AST equivalents generated from Racket AST.
    """
    def visit_Call(self, node):
        if isinstance(node.func, ast.Name) and node.func.id == 'racket_insert':
            racket_ast_node = node.args[0]
            file_name = racket_ast_node.value
            with open(file_name, 'r') as file:
                racket_code = file.read()
            racket_ast = tokenize_racket(racket_code)
            momo = racket_ast_to_python_ast(racket_ast)
            return momo
        return self.generic_visit(node)


def parse_combined_racket_python(python_file: str):
    # Instead of hardcoding 'code', we read from a provided Python file.
    with open(python_file, 'r') as f:
        code = f.read()

    parsed_code = ast.parse(code)
    transformed_code = RacketTransformer().visit(parsed_code)
    ast.fix_missing_locations(transformed_code)

    combined_code = compile(transformed_code, filename="<ast>", mode="exec")
    exec(combined_code)
