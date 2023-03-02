from expression.parser.Parser import FunctionNode, parse, ConstantNode, Node
from expression.parser.Printer import to_string


AVOID_KEY = 'muldivconv_avoid'


def div_to_mul(fn: Node):
    options = set()
    if isinstance(fn, FunctionNode) and fn.op == '/':
        lhs = fn.args[0]
        rhs = fn.args[1]
        if not isinstance(rhs, FunctionNode) or (isinstance(rhs, FunctionNode) and not rhs.annotations.get(AVOID_KEY, False)):
            rhs_inverted = FunctionNode('/', [ConstantNode(1), rhs], {AVOID_KEY: True})
            _fn = FunctionNode('*', [lhs, rhs_inverted])
            options.add(_fn)
    return options


def mul_to_div(fn: Node):
    options = set()
    if isinstance(fn, FunctionNode) and fn.op == '*':
        lhs = fn.args[0]
        rhs = fn.args[1]
        if not isinstance(rhs, FunctionNode) or (isinstance(rhs, FunctionNode) and not rhs.annotations.get(AVOID_KEY, False)):
            rhs_negated = FunctionNode('/', [ConstantNode(1), rhs], {AVOID_KEY: True})
            _fn = FunctionNode('/', [lhs, rhs_negated])
            options.add(_fn)
    return options


if __name__ == '__main__':
    for r in mul_to_div(parse('5*4')):
        print(f'{to_string(r)}')
    for r in div_to_mul(parse('5/2')):
        print(f'{to_string(r)}')