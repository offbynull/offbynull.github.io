from expression.parser.Parser import FunctionNode, parse
from expression.parser.Printer import to_string
from expression.TermExtractor import pull_terms


def distributive(fn: FunctionNode):
    def _attempt(arg1, arg2):
        nested_terms = pull_terms(arg2)
        distributed_n = None
        for term in nested_terms:
            _fn = FunctionNode('*', [arg1, term])
            if distributed_n is None:
                distributed_n = _fn
            else:
                distributed_n = FunctionNode('+', [distributed_n, _fn])
        return {distributed_n}
    if fn.op != '*':
        return set()
    options = set()
    options |= _attempt(fn.args[0], fn.args[1])
    options |= _attempt(fn.args[1], fn.args[0])
    return options


def undistributive(fn: FunctionNode):
    def _attempt(arg1, arg2):
        if isinstance(arg1, FunctionNode) and arg1.op == '*' and isinstance(arg2, FunctionNode) and arg2.op == '*':
            if arg1.args[0] == arg2.args[0]:
                _fn = FunctionNode(
                    '*',
                    [
                        arg1.args[0],
                        FunctionNode('+', [arg1.args[1], arg2.args[1]])
                    ]
                )
                return {_fn}
        return set()
    if fn.op not in '+':
        return set()
    options = set()
    options |= _attempt(fn.args[0], fn.args[1])
    options |= _attempt(fn.args[1], fn.args[0])
    return options


if __name__ == '__main__':
    # tree = parse('(x+1)*(2+7+(5*6))')
    # tree = parse('(x+1)*3')
    # result = distributive(tree)
    tree = parse('(x+1)*2+(x+1)*3')
    result = undistributive(tree)
    for r in result:
        print(f'{to_string(r)}')
