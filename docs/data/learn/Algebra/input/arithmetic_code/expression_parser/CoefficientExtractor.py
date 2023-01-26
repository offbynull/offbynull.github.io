from fractions import Fraction

from expression_parser.Parser import VariableNode, FunctionNode, parse


def pull_coefficient(term_n: FunctionNode | VariableNode | Fraction):
    if isinstance(term_n, VariableNode):
        return Fraction(1)
    elif isinstance(term_n, Fraction):
        return term_n
    if term_n.op == '*':
        if isinstance(term_n.args[0], Fraction) and isinstance(term_n.args[1], Fraction):
            raise ValueError('Simplify first')
        elif isinstance(term_n.args[0], Fraction):
            return term_n.args[0]
        elif isinstance(term_n.args[1], Fraction):
            return term_n.args[1]
        else:
            raise ValueError('Simplify first')
    else:
        return Fraction(1)


if __name__ == '__main__':
    # tree = parse('5 + -4 ^ x + 3 * 8 / log(2, 32) - 2 - y')
    # tree = parse('2*(2*4*x^2)')
    tree = parse('16*x^2')
    coefficient = pull_coefficient(tree)
    print(f'{coefficient}')
