from expression.Node import Node, ConstantNode, FunctionNode
from expression.parser.Parser import parse
from expression.parser.Printer import to_string


def exponent_quotient(fn: Node):
    if not isinstance(fn, FunctionNode):
        return set()
    if fn.op == '/':
        l_arg = fn.args[0]
        r_arg = fn.args[1]
        if isinstance(l_arg, FunctionNode) and l_arg.op == '^' and isinstance(r_arg, FunctionNode) and r_arg.op == '^'\
                and l_arg.args[0] == r_arg.args[0]:
            if isinstance(l_arg.args[1], ConstantNode) and isinstance(r_arg.args[1], ConstantNode):
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
                        ConstantNode(1),
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


def unexponent_quotient(n: Node):
    if not isinstance(n, FunctionNode):
        return set()
    if n.op == '^':
        l_arg = n.args[0]
        r_arg = n.args[1]
        if isinstance(r_arg, FunctionNode) and r_arg.op == '-':
            ret = FunctionNode(
                '/',
                [
                    FunctionNode('^', [l_arg, r_arg.args[0]]),
                    FunctionNode('^', [l_arg, r_arg.args[1]])
                ]
            )
            return {ret}
    elif n.op == '/' and n.args[0] == 1:
        _fn = n.args[1]
        if isinstance(_fn, FunctionNode) and _fn.op == '^':
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
