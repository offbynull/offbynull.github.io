import math
from math import sin, cos, tan, asin, acos, atan, log

from expression.Node import Node, ConstantNode, VariableNode, FunctionNode


def evaluate(n: Node, vars: dict[str, float | int]):
    if isinstance(n, ConstantNode):
        return n.value
    elif isinstance(n, VariableNode):
        if n.name == 'pi':
            return math.pi
        else:
            return vars[n.name]
    elif isinstance(n, FunctionNode):
        if n.op == '+':
            return evaluate(n.args[0], vars) + evaluate(n.args[1], vars)
        elif n.op == '-':
            return evaluate(n.args[0], vars) - evaluate(n.args[1], vars)
        elif n.op == '*':
            return evaluate(n.args[0], vars) * evaluate(n.args[1], vars)
        elif n.op == '/':
            return evaluate(n.args[0], vars) / evaluate(n.args[1], vars)
        elif n.op == '^':
            return evaluate(n.args[0], vars) ** evaluate(n.args[1], vars)
        elif n.op == 'abs':
            return abs(evaluate(n.args[0], vars))
        elif n.op == 'sin':
            return sin(evaluate(n.args[0], vars))
        elif n.op == 'cos':
            return cos(evaluate(n.args[0], vars))
        elif n.op == 'tan':
            return tan(evaluate(n.args[0], vars))
        elif n.op == 'arcsin':
            try:
                return asin(evaluate(n.args[0], vars))
            except ValueError:
                return math.nan
        elif n.op == 'arccos':
            try:
                return acos(evaluate(n.args[0], vars))
            except ValueError:
                return math.nan
        elif n.op == 'arctan':
            try:
                return atan(evaluate(n.args[0], vars))
            except ValueError:
                return math.nan
        elif n.op == 'cot':
            return 1/tan(evaluate(n.args[0], vars))
        elif n.op == 'sec':
            return 1/cos(evaluate(n.args[0], vars))
        elif n.op == 'csc':
            return 1/sin(evaluate(n.args[0], vars))
        elif n.op == 'log':
            try:
                return log(evaluate(n.args[1], vars)) / log(evaluate(n.args[0], vars))
            except ValueError:
                return math.nan
