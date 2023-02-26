from fractions import Fraction

from expression.parser.Parser import FunctionNode, parse, VariableNode
from expression.parser.Printer import to_string


AVOID_KEY = 'muldivconv_avoid'


def div_to_mul(fn: FunctionNode):
    options = {fn}
    if fn.op == '/':
        lhs = fn.args[0]
        rhs = fn.args[1]
        if not isinstance(rhs, FunctionNode) or (isinstance(rhs, FunctionNode) and not rhs.annotations.get(AVOID_KEY, False)):
            rhs_inverted = FunctionNode('/', [Fraction(1), rhs], {AVOID_KEY: True})
            _fn = FunctionNode('*', [lhs, rhs_inverted])
            options.add(_fn)
    return options


def mul_to_div(fn: FunctionNode):
    options = {fn}
    if fn.op == '*':
        lhs = fn.args[0]
        rhs = fn.args[1]
        if not isinstance(rhs, FunctionNode) or (isinstance(rhs, FunctionNode) and not rhs.annotations.get(AVOID_KEY, False)):
            rhs_negated = FunctionNode('/', [Fraction(1), rhs], {AVOID_KEY: True})
            _fn = FunctionNode('/', [lhs, rhs_negated])
            options.add(_fn)
    return options


if __name__ == '__main__':
    r = parse('5*4')
    print(f'{[to_string(x) for x in mul_to_div(r)]}')
    r = parse('5/2')
    print(f'{[to_string(x) for x in div_to_mul(r)]}')
