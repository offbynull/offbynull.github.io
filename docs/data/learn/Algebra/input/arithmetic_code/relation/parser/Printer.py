import expression.parser.Printer
from relation.Relation import Relation
from relation.parser.Parser import parse


def to_string(r: Relation):
    return expression.parser.Printer.to_string(r.lhs) + r.op + expression.parser.Printer.to_string(r.rhs)


if __name__ == '__main__':
    r = parse('5 + -4 ^ x + 3/5 <= 8 / log(2, 32)')
    print(f'{to_string(r)}')
