from fractions import Fraction

from expression.Utils import swap_variables, extract_variables
from expression.parser.Parser import FunctionNode, VariableNode, parse
from expression.Rearranger import simplify


def is_solution(
        lhs: FunctionNode | VariableNode | Fraction,
        rhs: FunctionNode | VariableNode | Fraction,
        var_replacements: dict[VariableNode, Fraction]
):
    lhs = swap_variables(lhs, var_replacements)
    lhs, _ = simplify(lhs)
    rhs = swap_variables(rhs, var_replacements)
    rhs, _ = simplify(rhs)
    if not isinstance(lhs, Fraction) or not isinstance(rhs, Fraction):
        raise ValueError(f'Missing variable replacements = {extract_variables(lhs) | extract_variables(rhs)}')
    return lhs == rhs


if __name__ == '__main__':
    tree_lhs = parse('4*x-2')
    tree_rhs = parse('2*x+1')
    solved = is_solution(tree_lhs, tree_rhs, {'x': Fraction(3, 2)})
    print(f'{solved}')
