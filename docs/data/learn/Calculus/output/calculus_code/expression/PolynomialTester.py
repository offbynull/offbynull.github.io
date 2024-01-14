from fractions import Fraction

from expression.Node import Node, FunctionNode, VariableNode
from expression.Utils import extract_terms
from expression.parser.Parser import parse


def is_monomial(n: Node):
    if isinstance(n, VariableNode) or isinstance(n, Fraction):
        return True
    elif isinstance(n, FunctionNode):
        if n.op == '*':
            return is_monomial(n.args[0]) and is_monomial(n.args[1])
        elif n.op == '^'\
                and isinstance(n.args[0], VariableNode)\
                and isinstance(n.args[1], Fraction) and n.args[1] >= 0:
            return True
        else:
            return False
    else:
        raise ValueError('???')


def is_polynomial(n: Node):
    terms = extract_terms(n)
    return all(is_monomial(t) for t in terms)


if __name__ == '__main__':
    tree = parse('5*x^3*x*y^2')
    print(f'{is_monomial(tree)}')
    tree = parse('5*x^-3*x*y^2')
    print(f'{is_monomial(tree)}')
    tree = parse('5*x^3+x*y^2')
    print(f'{is_monomial(tree)}')

    tree = parse('5*x^3*x*y^2 + 7')
    print(f'{is_polynomial(tree)}')