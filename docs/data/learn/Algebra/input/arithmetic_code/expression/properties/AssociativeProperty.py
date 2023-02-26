from expression.parser.Parser import FunctionNode, parse
from expression.parser.Printer import to_string


def associative(fn: FunctionNode):
    variations = set()
    if fn.op in '+*':
        variations.add(fn)
        l_arg = fn.args[0]
        r_arg = fn.args[1]
        if isinstance(l_arg, FunctionNode) and l_arg.op == fn.op:
            _fn = FunctionNode(
                fn.op,
                [
                    l_arg.args[0],
                    FunctionNode(fn.op, [l_arg.args[1], r_arg])
                ],
                fn.annotations
            )
            variations.add(_fn)
        if isinstance(r_arg, FunctionNode) and r_arg.op == fn.op:
            _fn = FunctionNode(
                fn.op,
                [
                    FunctionNode(fn.op, [l_arg, r_arg.args[0]]),
                    r_arg.args[1]
                ],
                fn.annotations
            )
            variations.add(_fn)
    return variations



if __name__ == '__main__':
    tree = parse('x+3+y*5+z')
    tree.annotations['x'] = 'hi'
    result = associative(tree)
    for r in result:
        print(f'{to_string(r)} {r.annotations}')