from expression.Node import Node, ConstantNode, FunctionNode
from expression.parser.Parser import parse
from expression.parser.Printer import to_string


def from_one_exponent(n: Node):
    if isinstance(n, FunctionNode) and n.op == '^':
        l_arg = n.args[0]
        r_arg = n.args[1]
        if r_arg == 1:
            return {l_arg}
    return set()


def to_one_exponent(fn: Node):
    return {FunctionNode('^', [fn, ConstantNode(1)])}


if __name__ == '__main__':
    for r in from_one_exponent(parse('x^1')):
        print(f'{to_string(r)}')
    for r in to_one_exponent(parse('x')):
        print(f'{to_string(r)}')
        for r1 in to_one_exponent(r):
            print(f'>>{to_string(r)}')