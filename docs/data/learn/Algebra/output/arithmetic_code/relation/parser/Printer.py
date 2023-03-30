import expression.parser.Printer
from relation.Relation import Relation, RelationWithDomain
from relation.parser.Parser import parse


def to_string(r: Relation | RelationWithDomain):
    if isinstance(r, Relation):
        return expression.parser.Printer.to_string(r.lhs) + r.op + expression.parser.Printer.to_string(r.rhs)
    else:
        ret = to_string(r.relation)
        if r.domains:
            ret += f' if {", ".join(to_string(_r) for _r in r.domains)}'
        return ret


if __name__ == '__main__':
    r = parse('5 + -4 ^ x + 3/5 <= 8 / log(2, 32)')
    print(f'{to_string(r)}')
