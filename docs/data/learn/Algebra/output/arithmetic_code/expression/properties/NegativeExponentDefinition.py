from expression.parser.Parser import FunctionNode, parse, ConstantNode, Node
from expression.parser.Printer import to_string


def from_negative_exponent(n: Node):
    if isinstance(n, FunctionNode) and n.op == '^':
        l_arg = n.args[0]
        r_arg = n.args[1]
        if isinstance(r_arg, ConstantNode) and r_arg < 0:
            ret = FunctionNode(
                '/',
                [
                    ConstantNode(1),
                    FunctionNode('^', [l_arg, -r_arg])
                ]
            )
            return {ret}
        elif isinstance(r_arg, FunctionNode) and r_arg.op == '*' and r_arg.args[0] == -1:
            ret = FunctionNode(
                '/',
                [
                    ConstantNode(1),
                    FunctionNode('^', [l_arg, r_arg.args[1]])
                ]
            )
            return {ret}
    return set()


def to_negative_exponent(fn: Node):
    if isinstance(fn, FunctionNode) and fn.op == '/' and fn.args[0] == 1:
        _fn = fn.args[1]
        if isinstance(_fn, FunctionNode) and _fn.op == '^':
            l_arg = _fn.args[0]
            r_arg = _fn.args[1]
            if isinstance(r_arg, ConstantNode) and r_arg > 0:
                ret = FunctionNode('^', [l_arg, -r_arg])
                return {ret}
            else:
                ret = FunctionNode(
                    '^',
                    [
                        l_arg,
                        FunctionNode('*', [ConstantNode(-1.0), r_arg])
                    ]
                )
                return {ret}
    return set()


if __name__ == '__main__':
    for r in from_negative_exponent(parse('x^-5')):
        print(f'{to_string(r)}')
    for r in from_negative_exponent(parse('x^-y')):
        print(f'{to_string(r)}')
    for r in to_negative_exponent(parse('1/(x^5)')):
        print(f'{to_string(r)}')
    for r in to_negative_exponent(parse('1/(x^y)')):
        print(f'{to_string(r)}')