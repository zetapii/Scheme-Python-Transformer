import ast
from utils import raise_parse_error
from typing import Any

# Racket AST to Python AST Converter
def racket_ast_to_python_ast(racket_ast: Any) -> ast.AST:
    if isinstance(racket_ast, bool):
        return ast.Constant(value=racket_ast)
    if isinstance(racket_ast, (int, float)):
        return ast.Constant(value=racket_ast)
    if isinstance(racket_ast, str):
        return ast.Name(id=racket_ast, ctx=ast.Load())
    if not isinstance(racket_ast, list):
        raise ValueError(f"Invalid expression: {racket_ast}")

    operator = racket_ast[0]

    if operator == '+':
        return ast.BinOp(
            left=racket_ast_to_python_ast(racket_ast[1]),
            op=ast.Add(),
            right=racket_ast_to_python_ast(racket_ast[2]),
        )
    elif operator == '-':
        return ast.BinOp(
            left=racket_ast_to_python_ast(racket_ast[1]),
            op=ast.Sub(),
            right=racket_ast_to_python_ast(racket_ast[2]),
        )
    elif operator == '*':
        return ast.BinOp(
            left=racket_ast_to_python_ast(racket_ast[1]),
            op=ast.Mult(),
            right=racket_ast_to_python_ast(racket_ast[2]),
        )
    elif operator == '/':
        return ast.BinOp(
            left=racket_ast_to_python_ast(racket_ast[1]),
            op=ast.Div(),
            right=racket_ast_to_python_ast(racket_ast[2]),
        )
    elif operator in ['<', '>', '==']:
        op_mapping = {
            '<': ast.Lt(),
            '>': ast.Gt(),
            '==': ast.Eq()
        }
        return ast.Compare(
            left=racket_ast_to_python_ast(racket_ast[1]),
            ops=[op_mapping[operator]],
            comparators=[racket_ast_to_python_ast(racket_ast[2])],
        )
    elif operator == 'if':
        return ast.IfExp(
            test=racket_ast_to_python_ast(racket_ast[1]),
            body=racket_ast_to_python_ast(racket_ast[2]),
            orelse=racket_ast_to_python_ast(racket_ast[3]),
        )
    elif operator == 'assume':
        bindings = racket_ast[1]
        body = racket_ast[2]
        if isinstance(bindings, list):
            assignment_nodes = []
            for bind in bindings:
                if len(bind) == 2 and isinstance(bind[0], str):
                    target = ast.Name(id=bind[0], ctx=ast.Store())
                    value = racket_ast_to_python_ast(bind[1])
                    assignment_nodes.append(ast.Assign(targets=[target], value=value))
                else:
                    raise ValueError("Invalid binding format in assume")
            return ast.Call(
                func=ast.Lambda(
                    args=ast.arguments(
                        args=[ast.arg(arg=bind[0], annotation=None) for bind in bindings],
                        posonlyargs=[],
                        vararg=None,
                        kwonlyargs=[],
                        kw_defaults=[],
                        defaults=[racket_ast_to_python_ast(bind[1]) for bind in bindings],
                        kwarg=None,

                    ),
                    body=racket_ast_to_python_ast(body),

                ),
                args=[],
                keywords=[]
            )
        else:
            raise ValueError("Invalid bindings in assume")

        
    elif operator == 'proc':
        if len(racket_ast) == 3:
            args_list = [ast.arg(arg=arg_name, annotation=None) for arg_name in racket_ast[1]]
            return ast.Lambda(
                args=ast.arguments(
                    args=args_list,
                    posonlyargs=[],
                    vararg=None,
                    kwonlyargs=[],
                    kw_defaults=[],
                    defaults=[],
                    kwarg=None,
                ),
                body=racket_ast_to_python_ast(racket_ast[2]),
            )
        func_name = racket_ast[1]
        arg_name = racket_ast[2]
        body_expr = racket_ast[3]

        func_args = ast.arguments(
            args=[ast.arg(arg=arg_name, annotation=None)],
            posonlyargs=[],
            vararg=None,
            kwonlyargs=[], 
            kw_defaults=[], 
            defaults=[]
        )

        func_body = [ast.Return(value=racket_ast_to_python_ast(body_expr))]

        return ast.FunctionDef(
            name=func_name,
            args=func_args,
            body=func_body,
            decorator_list=[]
        )
    else:
        raise ValueError(f"Unknown operator: {operator}")
