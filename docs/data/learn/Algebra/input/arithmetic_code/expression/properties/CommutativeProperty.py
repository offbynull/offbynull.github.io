from expression.parser.Parser import FunctionNode, parse, Node
from expression.parser.Printer import to_string


def commutative(fn: Node):
    if not isinstance(fn, FunctionNode):
        return set()
    variations = set()
    if fn.op in '+*':
        l_arg = fn.args[0]
        r_arg = fn.args[1]
        if (isinstance(l_arg, FunctionNode) and l_arg.op == fn.op) \
                or (isinstance(r_arg, FunctionNode) and r_arg.op == fn.op):
            variations.add(fn)
            _fn = FunctionNode(
                fn.op,
                fn.args[::-1],
                fn.annotations
            )
            variations.add(_fn)
    return variations



if __name__ == '__main__':
    tree = parse('(x*3)*y')
    tree.annotations['x'] = 'hi'
    result = commutative(tree)
    for r in result:
        print(f'{to_string(r)} {r.annotations}')