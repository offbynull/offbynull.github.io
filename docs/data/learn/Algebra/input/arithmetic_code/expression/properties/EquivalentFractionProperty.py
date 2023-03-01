from expression.parser.Parser import FunctionNode, parse, Node
from expression.parser.Printer import to_string


def equivalent_fraction(fn: Node):
    if not isinstance(fn, FunctionNode):
        return set()
    if fn.op == '/':
        l_arg = fn.args[0]
        r_arg = fn.args[1]
        if isinstance(l_arg, FunctionNode) and l_arg.op == '*' and isinstance(r_arg, FunctionNode) and r_arg.op == '*' \
                and l_arg.args[1] == r_arg.args[1]:
            ret = FunctionNode(
                '*',
                [
                    FunctionNode('/', [l_arg.args[0], r_arg.args[0]]),
                    FunctionNode('/', [l_arg.args[1], r_arg.args[1]])
                ]
            )
            return {ret}
    return set()


def unequivalent_fraction(fn: Node):
    if not isinstance(fn, FunctionNode):
        return set()
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
