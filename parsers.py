from typing import List, Any
from utils import raise_parse_error, is_id, is_binop, is_unaryop
from ast_classes import AST, Bind, Bool, Num, IdRef, Ifte, Assume, Proc, UnaryOp, BinOp
import re

def parse_bindings(bindings: List[Any]) -> List[Bind]:
    if not bindings:
        return []
    first, *rest = bindings
    if isinstance(first, list) and len(first) == 2 and is_id(first[0]):
        return [Bind(first[0], parse(first[1]))] + parse_bindings(rest)
    raise_parse_error("Invalid binding format")

def parse(exp: Any) -> AST:
    if isinstance(exp, bool):
        return Bool(exp)
    if isinstance(exp, (int, float)):
        return Num(exp)
    if is_id(exp):
        return IdRef(exp)
    if not isinstance(exp, list):
        raise_parse_error(f"Invalid expression: {exp}")
    if not exp:
        raise_parse_error("Empty expression")

    operator = exp[0]
    if operator == 'proc':
        if len(exp) == 4 and is_id(exp[1]):
            return Proc(var=exp[2], body=parse(exp[3]), id=exp[1])
        raise_parse_error("Invalid proc expression")
    if operator in {'if', 'ifte'}:
        if len(exp) == 4:
            return Ifte(parse(exp[1]), parse(exp[2]), parse(exp[3]))
        raise_parse_error("Invalid if expression")
    if operator == 'assume':
        if len(exp) >= 3:
            bindings = exp[1]
            body = exp[2]
            if isinstance(bindings, list):
                return Assume(parse_bindings(bindings), parse(body))
            raise_parse_error("Invalid bindings in assume")
        raise_parse_error("Invalid assume expression")
    if is_unaryop(operator):
        if len(exp) == 2:
            from utils import op_to_ast
            return UnaryOp(op_to_ast(operator), parse(exp[1]))
        raise_parse_error("Invalid unary operation")
    if is_binop(operator):
        if len(exp) == 3:
            from utils import op_to_ast
            return BinOp(op_to_ast(operator), parse(exp[1]), parse(exp[2]))
        raise_parse_error("Invalid binary operation")
    raise_parse_error(f"Unknown expression type: {exp}")

def tokenize_racket(racket_code: str) -> Any:
    tokens = re.findall(r'\(|\)|[^\s()]+', racket_code)
    def parse_tokens(tokens):
        if not tokens:
            raise SyntaxError("Unexpected EOF while reading")
        token = tokens.pop(0)
        if token == '(':
            expr = []
            while tokens[0] != ')':
                expr.append(parse_tokens(tokens))
            tokens.pop(0)  # Remove ')'
            return expr
        elif token == ')':
            raise SyntaxError("Unexpected )")
        else:
            if token.isdigit():
                return int(token)
            try:
                return float(token)
            except ValueError:
                return token
    return parse_tokens(tokens)
