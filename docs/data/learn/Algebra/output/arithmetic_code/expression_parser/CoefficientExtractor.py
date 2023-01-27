import ntpath
from fractions import Fraction

from expression_parser.Parser import VariableNode, FunctionNode, parse


def is_variable_part(n: FunctionNode | VariableNode | Fraction):
    if isinstance(n, FunctionNode):
        for a in n.args:
            if is_variable_part(a):
                return True
    elif isinstance(n, VariableNode):
        return True
    return False

def is_numeric_part(n: FunctionNode | VariableNode | Fraction):
    if isinstance(n, Fraction):
        return True
    return False

# Must be a single term to work.
# Term must be simplified to work (e.g. simplify 2*2*4*x^2 to 16*x^2)
# Coefficient must be first item in the list (e.g. 16*x^2 vs x^2*16)
def pull_coefficient(term_n: FunctionNode | VariableNode | Fraction):
    if isinstance(term_n, VariableNode):
        return Fraction(1)
    elif isinstance(term_n, Fraction):
        return term_n
    if term_n.op == '*':
        if term_n.args[0] and is_numeric_part(term_n.args[1]):
            return term_n.args[1]
        elif is_numeric_part(term_n.args[0]) and is_variable_part(term_n.args[1]):
            return term_n.args[0]
        else:
            return Fraction(1)
    else:
        return Fraction(1)


if __name__ == '__main__':
    # tree = parse('5 + -4 ^ x + 3 * 8 / log(2, 32) - 2 - y')
    tree = parse('2*(2*4*x^2)')
    # tree = parse('16*x^2')
    coefficient = pull_coefficient(tree)
    print(f'{coefficient}')
