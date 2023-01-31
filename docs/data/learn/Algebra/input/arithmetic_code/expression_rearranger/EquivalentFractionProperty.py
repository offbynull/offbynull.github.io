from fractions import Fraction

from expression_parser.Parser import FunctionNode, parse, VariableNode
from expression_parser.Printer import to_string
from expression_rearranger import AssociativeProperty


def equivalent_fraction(fn: FunctionNode):
    if fn.op == '/':
        l_arg = fn.args[0]
        r_arg = fn.args[1]
        if isinstance(l_arg, FunctionNode) and l_arg.op == '*' and isinstance(r_arg, FunctionNode) and r_arg.op == '*' \
                and l_arg.args[1] == r_arg.args[1]:
            ret = FunctionNode('/', [l_arg.args[0], r_arg.args[0]])
            return {ret}
    return set()


def unequivalent_fraction(fn: FunctionNode):
    if fn.op == '*':
        l_arg = fn.args[0]
        r_arg = fn.args[1]
        if isinstance(l_arg, FunctionNode) and l_arg.op == '/' and isinstance(r_arg, FunctionNode) and l_arg.op == '/':
            ret = FunctionNode(
                '/',
                [
                    FunctionNode('*', [l_arg.args[0], r_arg.args[0]]),
                    FunctionNode('*', [l_arg.args[1], r_arg.args[1]])
                ]
            )
            return {ret}
    return set()


if __name__ == '__main__':
    for r in equivalent_fraction(parse('(x*c)/(y*c)')):
        print(f'{to_string(r)}')
    for r in unequivalent_fraction(parse('(x/y)*(c/c)')):
        print(f'{to_string(r)}')
    for r in unequivalent_fraction(parse('(x/y)*c')):
        print(f'{to_string(r)}')