from fractions import Fraction

from expression.parser.Parser import FunctionNode, parse
from expression.parser.Printer import to_string


def negative_exponent(fn: FunctionNode):
    if fn.op == '^':
        l_arg = fn.args[0]
        r_arg = fn.args[1]
        if isinstance(r_arg, Fraction) and r_arg < Fraction(0):
            ret = FunctionNode(
                '/',
                [
                    Fraction(1),
                    FunctionNode('^', [l_arg, -r_arg])
                ]
            )
            return {ret}
        elif isinstance(r_arg, FunctionNode) and r_arg.op == '*' and r_arg.args[0] == Fraction(-1):
            ret = FunctionNode(
                '/',
                [
                    Fraction(1),
                    FunctionNode('^', [l_arg, r_arg.args[1]])
                ]
            )
            return {ret}
    return set()


def unnegative_exponent(fn: FunctionNode):
    if fn.op == '/' and fn.args[0] == Fraction(1):
        _fn = fn.args[1]
        if isinstance(_fn, FunctionNode) and _fn.op == '^':
            l_arg = _fn.args[0]
            r_arg = _fn.args[1]
            if isinstance(r_arg, Fraction) and r_arg > Fraction(0):
                ret = FunctionNode('^', [l_arg, -r_arg])
                return {ret}
            else:
                ret = FunctionNode(
                    '^',
                    [
                        l_arg,
                        FunctionNode('*', [Fraction(-1.0), r_arg])
                    ]
                )
                return {ret}
    return set()


if __name__ == '__main__':
    for r in negative_exponent(parse('x^-5')):
        print(f'{to_string(r)}')
    for r in negative_exponent(parse('x^-y')):
        print(f'{to_string(r)}')
    for r in unnegative_exponent(parse('1/(x^5)')):
        print(f'{to_string(r)}')
    for r in unnegative_exponent(parse('1/(x^y)')):
        print(f'{to_string(r)}')