from expression.Node import Node, ConstantNode, FunctionNode
from expression.parser.Parser import parse
from expression.parser.Printer import to_string


def zero_exponent(n: Node):
    if isinstance(n, FunctionNode) and n.op == '^':
        r_arg = n.args[1]
        if r_arg == 0:
            return {ConstantNode(1)}
    return set()



if __name__ == '__main__':
    for r in zero_exponent(parse('x^0')):
        print(f'{to_string(r)}')
