from typing import List

class AST:
    pass

class UnaryOp(AST):
    def __init__(self, op: str, rand: AST):
        self.op = op
        self.rand = rand

class BinOp(AST):
    def __init__(self, op: str, rand1: AST, rand2: AST):
        self.op = op
        self.rand1 = rand1
        self.rand2 = rand2

class Ifte(AST):
    def __init__(self, c: AST, t: AST, e: AST):
        self.c = c
        self.t = t
        self.e = e

class Num(AST):
    def __init__(self, n: float):
        self.n = n

class Bool(AST):
    def __init__(self, b: bool):
        self.b = b

class IdRef(AST):
    def __init__(self, sym: str):
        self.sym = sym

class Bind:
    def __init__(self, b_id: str, b_ast: AST):
        self.b_id = b_id
        self.b_ast = b_ast

class Assume(AST):
    def __init__(self, bindings: List[Bind], body: AST):
        self.bindings = bindings
        self.body = body

class Proc(AST):
    def __init__(self, id: str, var: str, body: AST):
        self.var = var
        self.body = body
        self.id = id

class Call(AST):
    def __init__(self, operator: AST, operand: AST):
        self.operator = operator
        self.operand = operand
