from expression.parser.Parser import FunctionNode, parse
from expression.parser.Printer import to_string


def exponent_quotient_to_power(fn: FunctionNode):
    if fn.op == '^':
        l_arg = fn.args[0]
        r_arg = fn.args[1]
        if isinstance(l_arg, FunctionNode) and l_arg.op == '/':
            ret = FunctionNode(
                '/',
                [
                    FunctionNode('^', [l_arg.args[0], r_arg]),
                    FunctionNode('^', [l_arg.args[1], r_arg])
                ]
            )
            return {ret}
    return set()


def unexponent_product_to_power(fn: FunctionNode):
    if fn.op == '/':
        l_arg = fn.args[0]
        r_arg = fn.args[1]
        if isinstance(l_arg, FunctionNode) and l_arg.op == '^'\
                and isinstance(r_arg, FunctionNode) and r_arg.op == '^'\
                and l_arg.args[1] == r_arg.args[1]:
            ret = FunctionNode(
                '^',
                [
                    FunctionNode('/', [l_arg.args[0], r_arg.args[0]]),
                    r_arg.args[1]
                ]
            )
            return {ret}
    return set()


if __name__ == '__main__':
    for r in exponent_quotient_to_power(parse('(x/y)^3')):
        print(f'{to_string(r)}')
    for r in unexponent_product_to_power(parse('(x^3)/(y^3)')):
        print(f'{to_string(r)}')
