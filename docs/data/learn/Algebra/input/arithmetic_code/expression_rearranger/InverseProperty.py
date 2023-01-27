from fractions import Fraction

from expression_parser.Parser import FunctionNode, parse
from expression_parser.Printer import to_string


FIX ME FIX ME FIX ME
FIX ME FIX ME FIX ME
FIX ME FIX ME FIX ME
FIX ME FIX ME FIX ME
FIX ME FIX ME FIX ME
def inverse(fn: FunctionNode):
    assert fn.op in '+-*/'
    if fn.op == '+':
        if fn.args[0] != Fraction(0) and fn.args[1] == FunctionNode('*', [Fraction(-1), fn.args[0]]):
            return {Fraction(1)}
        elif fn.args[1] != Fraction(0) and fn.args[0] == FunctionNode('*', [Fraction(-1), fn.args[1]]):
            return {Fraction(1)}
    elif fn.op == '-':
        if fn.args[0] == fn.args[1]:
            return {Fraction(0)}
    elif fn.op == '*':
        if fn.args[0] != Fraction(0) and fn.args[1] == FunctionNode('/', [Fraction(1), fn.args[0]]):
            return {Fraction(1)}
        elif fn.args[1] != Fraction(0) and fn.args[0] == FunctionNode('/', [Fraction(1), fn.args[1]]):
            return {Fraction(1)}
    elif fn.op == '/':
        if fn.args[0] == fn.args[1] and fn.args[0] != Fraction(0) and fn.args[1] != Fraction(0):
            return {Fraction(1)}



if __name__ == '__main__':
    tree = parse('1*x')
    result = inverse(tree)
    for r in result:
        print(f'{to_string(r)}')