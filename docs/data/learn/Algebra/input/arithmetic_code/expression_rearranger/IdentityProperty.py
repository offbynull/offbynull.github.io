from fractions import Fraction

from expression_parser.Parser import FunctionNode, parse
from expression_parser.Printer import to_string


def identity(fn: FunctionNode):
    if fn.op == '+':
        if fn.args[0] == Fraction(0):
            return {fn.args[1]}
        elif fn.args[1] == Fraction(0):
            return {fn.args[0]}
    elif fn.op == '-':
        if fn.args[1] == Fraction(0):
            return {fn.args[0]}
    elif fn.op == '*':
        if fn.args[0] == Fraction(1):
            return {fn.args[1]}
        elif fn.args[1] == Fraction(1):
            return {fn.args[0]}
    elif fn.op == '/':
        if fn.args[1] == Fraction(1):
            return {fn.args[0]}
    return set()


if __name__ == '__main__':
    # tree = parse('x*1')
    # tree = parse('x-0')
    # tree = parse('x/1')
    tree = parse('1*x')
    result = identity(tree)
    for r in result:
        print(f'{to_string(r)}')