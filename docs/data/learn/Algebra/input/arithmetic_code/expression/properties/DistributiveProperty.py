from expression.parser.Parser import FunctionNode, parse, Node
from expression.parser.Printer import to_string
from expression.Utils import extract_terms


def distributive(fn: Node):
    if not isinstance(fn, FunctionNode):
        return set()
    if fn.op != '*':
        return set()
    lhs = fn.args[0]
    rhs = fn.args[1]
    nested_terms = extract_terms(lhs)
    distributed_n = None
    for term in nested_terms:
        _fn = FunctionNode('*', [term, rhs])
        if distributed_n is None:
            distributed_n = _fn
        else:
            distributed_n = FunctionNode('+', [distributed_n, _fn])
    return {distributed_n}


def undistributive(fn: Node):
    if not isinstance(fn, FunctionNode):
        return set()
    if fn.op not in '+':
        return set()
    lhs = fn.args[0]
    rhs = fn.args[1]
    if isinstance(lhs, FunctionNode) and lhs.op == '*' and isinstance(rhs, FunctionNode) and rhs.op == '*':
        if lhs.args[0] == rhs.args[0]:
            _fn = FunctionNode(
                '*',
                [
                    lhs.args[0],
                    FunctionNode('+', [lhs.args[1], rhs.args[1]])
                ]
            )
            return {_fn}
    return set()


if __name__ == '__main__':
    for r in distributive(parse('(x+1)*3')):
        print(f'{to_string(r)}')
    for r in distributive(parse('(x+y+1)*3')):
        print(f'{to_string(r)}')
    for r in undistributive(parse('(x+1)*2+(x+1)*3')):
        print(f'{to_string(r)}')
    for r in undistributive(parse('(x+1)*(1+2)+(x+1)*3')):
        print(f'{to_string(r)}')
