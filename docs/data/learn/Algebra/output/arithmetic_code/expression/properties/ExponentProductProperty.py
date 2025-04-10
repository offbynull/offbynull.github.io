from expression.Node import Node, FunctionNode
from expression.parser.Parser import parse
from expression.parser.Printer import to_string


def exponent_product(n: Node):
    if not isinstance(n, FunctionNode):
        return set()
    if n.op == '*':
        l_arg = n.args[0]
        r_arg = n.args[1]
        if isinstance(l_arg, FunctionNode) and isinstance(r_arg, FunctionNode) and \
                l_arg.op == '^' and r_arg.op == '^' and\
                l_arg.args[0] == r_arg.args[0]:
            ret = FunctionNode(
                '^',
                [
                    l_arg.args[0],
                    FunctionNode('+', [l_arg.args[1], r_arg.args[1]])
                ]
            )
            return {ret}
    return set()


def unexponent_product(fn: Node):
    if not isinstance(fn, FunctionNode):
        return set()
    if fn.op == '^':
        l_arg = fn.args[0]
        r_arg = fn.args[1]
        if isinstance(r_arg, FunctionNode) and r_arg.op == '+':
            ret = FunctionNode(
                '*',
                [
                    FunctionNode('^', [l_arg, r_arg.args[0]]),
                    FunctionNode('^', [l_arg, r_arg.args[1]])
                ]
            )
            return {ret}
    return set()


if __name__ == '__main__':
    for r in exponent_product(parse('x^3*x^x')):
        print(f'{to_string(r)}')
    for r in unexponent_product(parse('x^(3+x)')):
        print(f'{to_string(r)}')