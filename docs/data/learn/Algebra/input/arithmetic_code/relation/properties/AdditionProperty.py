from expression.Exploder import ExplosionCache, simplify
from expression.Node import Node
from expression.parser.Parser import FunctionNode, parse
from relation.Relation import Relation, RelationWithDomain


def addition(rel_with_dom: RelationWithDomain, operand: Node, cache: ExplosionCache) -> set[RelationWithDomain]:
    operand, _ = simplify(operand, cache)  # this is necessary because it should remove unused variables
    options = set()
    rel = rel_with_dom.relation
    doms = rel_with_dom.domains
    _lhs = FunctionNode('+', [rel.lhs, operand])
    _rhs = FunctionNode('+', [rel.rhs, operand])
    _rel = Relation(rel.op, _lhs, _rhs)
    options.add(RelationWithDomain(_rel, doms))
    return options


if __name__ == '__main__':
    rel = RelationWithDomain(
        Relation('<', parse('x-2'), parse('0')),
        frozenset()
    )
    options = addition(rel, parse('x+x+x'), ExplosionCache())
    for rel in options:
        print(f'{rel}')
