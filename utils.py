import ast

class ExecNotImplemented(Exception):
    pass

def raise_exec_not_implemented():
    raise ExecNotImplemented("Not implemented")

class ParseError(Exception):
    pass

def raise_parse_error(msg: str):
    raise ParseError(msg)

def is_id(thing) -> bool:
    return isinstance(thing, str)

def is_expressible_value(thing) -> bool:
    return isinstance(thing, (int, float, bool))

def is_denotable_value(thing) -> bool:
    return isinstance(thing, (int, float, bool))

def op_to_ast(op: str) -> str:
    mapping = {
        '+': 'add',
        '-': 'sub',
        '*': 'mul',
        '/': 'div',
        '<': 'ltj',
        '==': 'eq',
        '!': 'neg'
    }
    return mapping.get(op, 'error')

def is_binop(op: str) -> bool:
    return op in {'+', '-', '*', '/', '<', '=='}

def is_unaryop(op: str) -> bool:
    return op == '!'
