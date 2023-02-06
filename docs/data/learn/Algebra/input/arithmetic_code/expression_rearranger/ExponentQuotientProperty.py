from fractions import Fraction

from expression_parser.Parser import FunctionNode, parse, VariableNode
from expression_parser.Printer import to_string
from expression_rearranger import AssociativeProperty


def exponent_quotient(fn: FunctionNode):
    if fn.op == '/':
        l_arg = fn.args[0]
        r_arg = fn.args[1]
        if isinstance(l_arg, FunctionNode) and l_arg.op == '^' and isinstance(r_arg, FunctionNode) and r_arg.op == '^'\
                and l_arg.args[0] == r_arg.args[0]:
            if isinstance(l_arg.args[1], Fraction) and isinstance(r_arg.args[1], Fraction):
                if l_arg.args[1] >= r_arg.args[1]:
                    ret = FunctionNode(
                        '^',
                        [
                            l_arg.args[0],
                            FunctionNode('-', [l_arg.args[1], r_arg.args[1]])
                        ]
                    )
                else:
                    ret = FunctionNode('/', [
                        Fraction(1),
                        FunctionNode(
                            '^',
                            [
                                l_arg.args[0],
                                FunctionNode('-', [r_arg.args[1], l_arg.args[1]])
                            ]
                        )
                    ])
                return {ret}
            else:
                ret = FunctionNode(
                    '^',
                    [
                        l_arg.args[0],
                        FunctionNode('-', [l_arg.args[1], r_arg.args[1]])
                    ]
                )
                return {ret}
    return set()


def unexponent_quotient(fn: FunctionNode):
    if fn.op == '^':
        l_arg = fn.args[0]
        r_arg = fn.args[1]
        if isinstance(r_arg, FunctionNode) and r_arg.op == '-':
            ret = FunctionNode(
                '/',
                [
                    FunctionNode('^', [l_arg, r_arg.args[0]]),
                    FunctionNode('^', [l_arg, r_arg.args[1]])
                ]
            )
            return {ret}
    elif fn.op == '/' and fn.args[0] == Fraction(1):
        _fn = fn.args[1]
        if _fn.op == '^':
            l_arg = _fn.args[0]
            r_arg = _fn.args[1]
            if isinstance(r_arg, FunctionNode) and r_arg.op == '-':
                ret = FunctionNode(
                    '/',
                    [
                        FunctionNode('^', [l_arg, r_arg.args[1]]),
                        FunctionNode('^', [l_arg, r_arg.args[0]])
                    ]
                )
                return {ret}
    return set()


if __name__ == '__main__':
    for r in exponent_quotient(parse('(x^z)/(x^2)')):
        print(f'{to_string(r)}')
    for r in exponent_quotient(parse('(x^3)/(x^2)')):
        print(f'{to_string(r)}')
    for r in exponent_quotient(parse('(x^2)/(x^3)')):
        print(f'{to_string(r)}')
    for r in unexponent_quotient(parse('x^(3-2)')):
        print(f'{to_string(r)}')
    for r in unexponent_quotient(parse('1/(x^(3-2))')):
        print(f'{to_string(r)}')
