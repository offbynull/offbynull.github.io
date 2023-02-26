from fractions import Fraction

from Factor import factor_fastest
from expression.parser.Parser import FunctionNode, parse
from expression.parser.Printer import to_string


def factor(fn: FunctionNode):
    assert fn.op in '+'
    arg1 = fn.args[0]
    arg2 = fn.args[1]
    if isinstance(arg1, FunctionNode) and arg1.op == '*' and isinstance(arg2, FunctionNode) and arg2.op == '*':
        p1 = arg1.args[0]
        p2 = arg2.args[0]
        if isinstance(p1, Fraction) and isinstance(p2, Fraction) \
                and p1.denominator == 1 and p2.denominator == 1:
            if p1 > 0:
                factors1 = factor_fastest(int(p1))
            elif p1 < 0:
                factors1 = factor_fastest(-int(p1))
                factors1 = {-f for f in factors1}
            else:
                return set()
            if p2 > 0:
                factors2 = factor_fastest(int(p2))
            elif p2 < 0:
                factors2 = factor_fastest(-int(p2))
                factors2 = {-f for f in factors2}
            else:
                return set()
            factor = max(factors1 & factors2)
            factor = Fraction(factor)
            _fn = FunctionNode(
                '*',
                [
                    factor,
                    FunctionNode(
                        '+',
                        [
                            FunctionNode('*', [p1 / factor, arg1.args[1]]),
                            FunctionNode('*', [p2 / factor, arg2.args[1]])
                        ]
                    )
                ]
            )
            return {_fn}
    return set()


if __name__ == '__main__':
    # tree = parse('(x+1)*(2+7+(5*6))')
    # tree = parse('(x+1)*3')
    # result = distributive(tree)
    # tree = parse('(x+1)*2+(x+1)*3')
    tree = parse('(2*x^2)+(6*x)')
    print(to_string(tree))
    result = factor(tree)
    for r in result:
        print(f'{to_string(r)}')
