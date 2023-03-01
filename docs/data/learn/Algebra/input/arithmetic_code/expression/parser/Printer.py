from fractions import Fraction

from expression.parser.Parser import FunctionNode, VariableNode, parse, ConstantNode, Node


def to_string(n: Node):
    if isinstance(n, ConstantNode):
        if isinstance(n.value, Fraction):
            n = n.value
            if n.denominator == 1:
                return str(n)
            else:
                return str(n.numerator) + ':' + str(n.denominator)
        elif isinstance(n.value, str):
            n = n.value
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
        else:
            raise ValueError()
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
