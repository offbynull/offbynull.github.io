from fractions import Fraction

from expression.parser.Parser import VariableNode, FunctionNode, parse


def negate(n: FunctionNode | VariableNode | Fraction):
    if isinstance(n, Fraction):
        return -n
    return FunctionNode('*', [Fraction(-1), n])

def pull_terms(n: FunctionNode | VariableNode | Fraction):
    if isinstance(n, VariableNode) or isinstance(n, Fraction):
        return [n]
    if n.op == '+':
        return pull_terms(n.args[0]) + pull_terms(n.args[1])
    elif n.op == '-':
        return pull_terms(n.args[0]) + [negate(n.args[1])]
    else:
        return [n]


if __name__ == '__main__':
    tree = parse('5 + -4 ^ x + 3 * 8 / log(2, 32) - 2 - y')
    terms = pull_terms(tree)
    for t in terms:
        print(f'{t}')
