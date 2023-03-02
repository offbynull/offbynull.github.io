from fractions import Fraction

from expression.parser.Parser import FunctionNode, parse, ConstantNode, Node
from expression.parser.Printer import to_string


AVOID_KEY = 'one_exp_avoid'


def from_one_exponent(fn: Node):
    if isinstance(fn, FunctionNode) and fn.op == '^':
        l_arg = fn.args[0]
        r_arg = fn.args[1]
        if r_arg == 1:
            return {l_arg}
    return set()


def to_one_exponent(fn: Node):
    if not fn.annotations.get(AVOID_KEY, False):
        return {FunctionNode('^', [fn, ConstantNode(1)], {AVOID_KEY: True})}
    return set()


if __name__ == '__main__':
    for r in from_one_exponent(parse('x^1')):
        print(f'{to_string(r)}')
    for r in to_one_exponent(parse('x')):
        print(f'{to_string(r)}')
        for r1 in to_one_exponent(r):
            print(f'>>{to_string(r)}')