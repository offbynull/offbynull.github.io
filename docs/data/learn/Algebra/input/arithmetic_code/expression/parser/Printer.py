from fractions import Fraction

from expression.parser.Parser import FunctionNode, VariableNode, parse


def to_string(n: FunctionNode | VariableNode | Fraction | str):
    if isinstance(n, Fraction):
        if n.denominator == 1:
            return str(n)
        else:
            return str(n.numerator) + ':' + str(n.denominator)
    elif isinstance(n, str):
        ret = '\''
        for c in n:
            if c == '\'':
                ret += '\\\''
            elif c == '\\':
                ret += '\\\\'
            else:
                ret += c
        ret += '\''
        return ret
    elif isinstance(n, VariableNode):
        return n.name
    elif isinstance(n, FunctionNode):
        if n.op in '*+/-^':
            return '(' + to_string(n.args[0]) + n.op + to_string(n.args[1]) + ')'
        else:
            return n.op + '(' + ','.join(to_string(a) for a in n.args) + ')'


if __name__ == '__main__':
    tree = parse('5 + -4 ^ x + 3:5 * 8 / log(2, 32)')
    print(f'{to_string(tree)}')
