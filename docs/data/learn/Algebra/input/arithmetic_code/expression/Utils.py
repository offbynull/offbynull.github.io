from fractions import Fraction

from expression.parser.Parser import FunctionNode, VariableNode, parse, Node, ConstantNode
from expression.parser.Printer import to_string


def swap_variables(
        n: Node,
        var_replacements: dict[VariableNode, ConstantNode]
) -> Node:
    if isinstance(n, VariableNode):
        if n in var_replacements:
            ret = var_replacements[n]
        else:
            ret = n
    elif isinstance(n, FunctionNode):
        ret = FunctionNode(
            n.op,
            [swap_variables(a, var_replacements) for a in n.args]
        )
    elif isinstance(n, ConstantNode):
        ret = n
    else:
        raise ValueError('???')
    return ret


def extract_variables(n: Node) -> set[str]:
    if isinstance(n, VariableNode):
        return {n.name}
    elif isinstance(n, FunctionNode):
        ret = set()
        for a in n.args:
            ret |= extract_variables(a)
        return ret
    elif isinstance(n, ConstantNode):
        return set()
    else:
        raise ValueError('???')


def extract_numeric_constants(n: Node) -> set[ConstantNode]:
    if isinstance(n, VariableNode):
        return set()
    elif isinstance(n, FunctionNode):
        ret = set()
        for a in n.args:
            ret |= extract_functions(a)
        return ret
    elif isinstance(n, ConstantNode) and isinstance(n.value, Fraction):
        return {n}
    else:
        raise ValueError('???')


def extract_functions(n: Node) -> set[FunctionNode]:
    if isinstance(n, VariableNode):
        return set()
    elif isinstance(n, FunctionNode):
        ret = {n}
        for a in n.args:
            ret |= extract_functions(a)
        return ret
    elif isinstance(n, ConstantNode):
        return set()
    else:
        raise ValueError('???')


def extract_all(n: Node) -> set[Node]:
    if isinstance(n, VariableNode):
        return {n}
    elif isinstance(n, FunctionNode):
        ret = {n}
        for a in n.args:
            ret |= extract_all(a)
        return ret
    elif isinstance(n, ConstantNode):
        return {n}
    else:
        raise ValueError('???')


def count_functions(n: Node) -> int:
    if isinstance(n, VariableNode):
        return 0
    elif isinstance(n, FunctionNode):
        return 1 + sum(count_functions(a) for a in n.args)
    elif isinstance(n, ConstantNode):
        return 0
    else:
        raise ValueError('???')


def negate(n: Node):
    if isinstance(n, ConstantNode):
        return -n
    return FunctionNode('*', [ConstantNode(-1), n])


def extract_terms(n: Node):
    if isinstance(n, VariableNode) or isinstance(n, ConstantNode):
        return [n]
    elif isinstance(n, FunctionNode):
        if n.op == '+':
            return extract_terms(n.args[0]) + extract_terms(n.args[1])
        elif n.op == '-':
            return extract_terms(n.args[0]) + [negate(n.args[1])]
        else:
            return [n]
    else:
        raise ValueError('???')


def extract_multipliers(n: Node):
    def __internal(_n: Node):
        if isinstance(_n, VariableNode):
            return [_n]
        elif isinstance(_n, ConstantNode):
            return [_n]
        elif isinstance(_n, FunctionNode):
            if _n.op == '*':
                return __internal(_n.args[0]) + __internal(_n.args[1])
            else:
                return [_n]
        else:
            raise ValueError('???')

    if isinstance(n, FunctionNode) and n.op == '*':
        return __internal(n)
    else:
        raise ValueError('Not multiplication')


if __name__ == '__main__':
    tree = parse('5 + -4 ^ x + 3 * 8 / log(2, 32) - 2 - y')
    print(f'{to_string(tree)}')
    print(f'{extract_variables(tree)}')
    print(f'{count_functions(tree)}')
    tree = swap_variables(tree, {VariableNode('x'): ConstantNode(1), VariableNode('y'): ConstantNode(2)})
    print(f'{to_string(tree)}')
    print(f'{extract_variables(tree)}')
    print(f'{count_functions(tree)}')
    tree = parse('5 + -4 ^ x + 3 * 8 / log(2, 32) - 2 - y')
    terms = extract_terms(tree)
    for t in terms:
        print(f'{t}')
    print('---')
    tree = parse('5*4*(x+1)+1')
    multipliers = extract_multipliers(tree)
    for m in multipliers:
        print(f'{m}')
