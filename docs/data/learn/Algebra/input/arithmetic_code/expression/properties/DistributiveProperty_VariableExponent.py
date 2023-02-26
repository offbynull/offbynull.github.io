from fractions import Fraction

from expression.parser.Parser import FunctionNode, parse, VariableNode
from expression.parser.Printer import to_string


def factor(fn: FunctionNode):
    assert fn.op in '+'
    arg1 = fn.args[0]
    arg2 = fn.args[1]
    if isinstance(arg1, FunctionNode) and arg1.op == '*' and isinstance(arg2, FunctionNode) and arg2.op == '*':
        p1 = arg1.args[0]
        p2 = arg2.args[0]
        if isinstance(p1, VariableNode) \
                and isinstance(p2, VariableNode) \
                and p1 == p2:
            _fn = FunctionNode(
                '*',
                [
                    p1,
                    FunctionNode('+', [arg1.args[1], arg2.args[1]])
                ]
            )
            return {_fn}
        elif isinstance(p1, VariableNode) \
                and (isinstance(p2, FunctionNode) and p2.op == '^' and isinstance(p2.args[0], VariableNode) and isinstance(p2.args[1], Fraction)) \
                and p1 == p2.args[0]:
            _fn = FunctionNode(
                '*',
                [
                    p1,
                    FunctionNode(
                        '+',
                        [
                            arg1.args[1],
                            FunctionNode('^', [p2.args[0], p2.args[1] - 1])
                        ]
                    )
                ]
            )
            return {_fn}
        elif (isinstance(p1, FunctionNode) and p1.op == '^' and isinstance(p1.args[0], VariableNode) and isinstance(p1.args[1], Fraction)) \
                and isinstance(p2, VariableNode) \
                and p1.args[0] == p2:
            _fn = FunctionNode(
                '*',
                [
                    p2,
                    FunctionNode(
                        '+',
                        [
                            FunctionNode('^', [p1.args[0], p1.args[1] - 1]),
                            arg2.args[1]
                        ]
                    )
                ]
            )
            return {_fn}
        elif (isinstance(p1, FunctionNode) and p1.op == '^' and isinstance(p1.args[0], VariableNode) and isinstance(p1.args[1], Fraction)) \
                and (isinstance(p2, FunctionNode) and p2.op == '^' and isinstance(p2.args[0], VariableNode) and isinstance(p2.args[1], Fraction)) \
                and p1.args[0] == p2.args[0]:
            _fn = FunctionNode(
                '*',
                [
                    p1,
                    FunctionNode(
                        '+',
                        [
                            FunctionNode('^', [p1.args[0], p1.args[1] - 1]),
                            FunctionNode('^', [p2.args[0], p2.args[1] - 1])
                        ]
                    )
                ]
            )
    return set()


if __name__ == '__main__':
    # tree = parse('(x+1)*(2+7+(5*6))')
    # tree = parse('(x+1)*3')
    # result = distributive(tree)
    # tree = parse('(x+1)*2+(x+1)*3')
    for r in factor(parse('(x*2)+(x*1)')):
        print(f'{to_string(r)}')
    for r in factor(parse('(x*2)+(x^3*1)')):
        print(f'{to_string(r)}')
    for r in factor(parse('(x^3*2)+(x*2)')):
        print(f'{to_string(r)}')