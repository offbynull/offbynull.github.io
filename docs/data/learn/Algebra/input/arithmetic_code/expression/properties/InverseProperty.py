from fractions import Fraction

from expression.parser.Parser import FunctionNode, parse, VariableNode
from expression.parser.Printer import to_string
from expression.properties import AssociativeProperty


def inverse(fn: FunctionNode):
    if fn.op == '+':
        for fn in AssociativeProperty.associative(fn):
            if isinstance(fn.args[0], FunctionNode) and fn.args[1] == FunctionNode('*', [Fraction(-1), fn.args[0]]):
                return {Fraction(0)}
            if isinstance(fn.args[0], VariableNode) and fn.args[1] == FunctionNode('*', [Fraction(-1), fn.args[0]]):
                return {Fraction(0)}
            elif isinstance(fn.args[0], Fraction) and fn.args[1] == -fn.args[0]:
                return {Fraction(0)}
    elif fn.op == '*':
        for fn in AssociativeProperty.associative(fn):
            if isinstance(fn.args[0], FunctionNode) and fn.args[1] == FunctionNode('/', [Fraction(1), fn.args[0]]):
                return {Fraction(1)}
            if isinstance(fn.args[0], VariableNode) and fn.args[1] == FunctionNode('/', [Fraction(1), fn.args[0]]):
                return {Fraction(1)}
            elif isinstance(fn.args[0], Fraction) and fn.args[0] != Fraction(0) and fn.args[1] == (1 / fn.args[0]):
                return {Fraction(1)}
    elif fn.op == '-':
        if fn.args[0] == fn.args[1]:
            return {Fraction(0)}
    elif fn.op == '/':
        if fn.args[0] == fn.args[1] and fn.args[0] != Fraction(0):
            return {Fraction(1)}
    return set()


if __name__ == '__main__':
    for r in inverse(parse('5*1:5')):
        print(f'{to_string(r)}')
    for r in inverse(parse('x*(1/x)')):
        print(f'{to_string(r)}')
    for r in inverse(parse('(x-9)*(1/(x-9))')):
        print(f'{to_string(r)}')