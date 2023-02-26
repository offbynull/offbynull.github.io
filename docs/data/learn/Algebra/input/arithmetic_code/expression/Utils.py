from fractions import Fraction

from expression.parser.Parser import FunctionNode, VariableNode, parse
from expression.parser.Printer import to_string


def swap_variables(
        n: FunctionNode | VariableNode | Fraction,
        var_replacements: dict[VariableNode, Fraction]
) -> FunctionNode | VariableNode | Fraction:
    if isinstance(n, VariableNode):
        if n in var_replacements:
            ret = var_replacements[n.name]
        else:
            ret = n
    elif isinstance(n, FunctionNode):
        ret = FunctionNode(
            n.op,
            [swap_variables(a, var_replacements) for a in n.args]
        )
    elif isinstance(n, Fraction):
        ret = n
    else:
        raise ValueError('???')
    return ret


def extract_variables(n: FunctionNode | VariableNode | Fraction) -> set[str]:
    if isinstance(n, VariableNode):
        return {n.name}
    elif isinstance(n, FunctionNode):
        ret = set()
        for a in n.args:
            ret |= extract_variables(a)
        return ret
    elif isinstance(n, Fraction):
        return set()
    else:
        raise ValueError('???')


def extract_numbers(n: FunctionNode | VariableNode | Fraction) -> set[Fraction]:
    if isinstance(n, VariableNode):
        return set()
    elif isinstance(n, FunctionNode):
        ret = set()
        for a in n.args:
            ret |= extract_functions(a)
        return ret
    elif isinstance(n, Fraction):
        return {n}
    else:
        raise ValueError('???')


def extract_functions(n: FunctionNode | VariableNode | Fraction) -> set[FunctionNode]:
    if isinstance(n, VariableNode):
        return set()
    elif isinstance(n, FunctionNode):
        ret = {n}
        for a in n.args:
            ret |= extract_functions(a)
        return ret
    elif isinstance(n, Fraction):
        return set()
    else:
        raise ValueError('???')


def extract_all(n: FunctionNode | VariableNode | Fraction) -> set[FunctionNode | VariableNode | Fraction]:
    if isinstance(n, VariableNode):
        return {n}
    elif isinstance(n, FunctionNode):
        ret = {n}
        for a in n.args:
            ret |= extract_all(a)
        return ret
    elif isinstance(n, Fraction):
        return {n}
    else:
        raise ValueError('???')


def count_functions(n: FunctionNode | VariableNode | Fraction) -> int:
    if isinstance(n, VariableNode):
        return 0
    elif isinstance(n, FunctionNode):
        return 1 + sum(count_functions(a) for a in n.args)
    elif isinstance(n, Fraction):
        return 0
    else:
        raise ValueError('???')


if __name__ == '__main__':
    tree = parse('5 + -4 ^ x + 3 * 8 / log(2, 32) - 2 - y')
    print(f'{to_string(tree)}')
    print(f'{extract_variables(tree)}')
    print(f'{count_functions(tree)}')
    tree = swap_variables(tree, {'x': Fraction(1), 'y': Fraction(2)})
    print(f'{to_string(tree)}')
    print(f'{extract_variables(tree)}')
    print(f'{count_functions(tree)}')
