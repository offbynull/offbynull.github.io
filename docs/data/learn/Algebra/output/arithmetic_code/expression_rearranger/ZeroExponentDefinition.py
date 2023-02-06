from fractions import Fraction

from expression_parser.Parser import FunctionNode, parse, VariableNode
from expression_parser.Printer import to_string
from expression_rearranger import AssociativeProperty


def zero_exponent(fn: FunctionNode):
    if fn.op == '^':
        r_arg = fn.args[1]
        if r_arg == Fraction(0):
            return {Fraction(1)}
    return set()



if __name__ == '__main__':
    for r in zero_exponent(parse('x^0')):
        print(f'{to_string(r)}')
