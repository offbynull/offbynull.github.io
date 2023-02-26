from expression.parser.Parser import FunctionNode, parse
from expression.parser.Printer import to_string


def commutative(fn: FunctionNode):
    variations = set()
    if fn.op in '+*':
        variations.add(fn)
        _fn = FunctionNode(
            fn.op,
            fn.args[::-1],
            fn.annotations
        )
        variations.add(_fn)
    return variations



if __name__ == '__main__':
    tree = parse('x+3*y')
    tree.annotations['x'] = 'hi'
    result = commutative(tree)
    for r in result:
        print(f'{to_string(r)} {r.annotations}')