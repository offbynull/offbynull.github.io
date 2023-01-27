from expression_parser.Parser import FunctionNode, parse
from expression_parser.Printer import to_string


def associative(fn: FunctionNode):
    assert fn.op in '+*'
    variations = {fn}
    l_arg = fn.args[0]
    r_arg = fn.args[1]
    if isinstance(fn.args[0], FunctionNode) and fn.args[0].op == fn.op:
        _fn = FunctionNode(
            fn.op,
            [
                l_arg.args[0],
                FunctionNode(fn.op, [l_arg.args[1], r_arg])
            ]
        )
        variations.add(_fn)
    if isinstance(fn.args[1], FunctionNode) and fn.args[1].op == fn.op:
        _fn = FunctionNode(
            fn.op,
            [
                FunctionNode(fn.op, [l_arg, r_arg.args[0]]),
                r_arg.args[1]
            ]
        )
        variations.add(_fn)
    return variations



if __name__ == '__main__':
    tree = parse('x+3+y*5+z')
    result = associative(tree)
    for r in result:
        print(f'{to_string(r)}')