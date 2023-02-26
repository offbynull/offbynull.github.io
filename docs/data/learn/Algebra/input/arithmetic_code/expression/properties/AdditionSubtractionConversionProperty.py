from fractions import Fraction

from expression.parser.Parser import FunctionNode, parse, VariableNode
from expression.parser.Printer import to_string


AVOID_KEY = 'addsubconv_avoid'


def sub_to_add(fn: FunctionNode):
    options = {fn}
    if fn.op == '-':
        lhs = fn.args[0]
        rhs = fn.args[1]
        if not isinstance(rhs, FunctionNode) or (isinstance(rhs, FunctionNode) and not rhs.annotations.get(AVOID_KEY, False)):
            rhs_negated = FunctionNode('*', [Fraction(-1), rhs], {AVOID_KEY: True})
            _fn = FunctionNode('+', [lhs, rhs_negated])
            options.add(_fn)
    return options


def add_to_sub(fn: FunctionNode):
    options = {fn}
    if fn.op == '+':
        lhs = fn.args[0]
        rhs = fn.args[1]
        if not isinstance(rhs, FunctionNode) or (isinstance(rhs, FunctionNode) and not rhs.annotations.get(AVOID_KEY, False)):
            rhs_negated = FunctionNode('*', [Fraction(-1), rhs], {AVOID_KEY: True})
            _fn = FunctionNode('-', [lhs, rhs_negated])
            options.add(_fn)
    return options


if __name__ == '__main__':
    r = parse('-2+(4*x)')
    print(f'{to_string(r)}')
    for r1 in sub_to_add(r):
        print(f'>>{to_string(r1)}')
        for r2 in add_to_sub(r1):
            print(f'>>>>{to_string(r2)}')
            for r3 in sub_to_add(r2):
                print(f'>>>>>>{to_string(r3)}')
                for r4 in add_to_sub(r3):
                    print(f'>>>>>>>>{to_string(r4)}')
    # for r in add_to_sub(parse('(4*x)+(-1*y)')):
    #     print(f'{to_string(r)}')
