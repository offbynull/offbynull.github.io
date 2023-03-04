from expression.Exploder import ExplosionCache, simplify
from expression.parser.Parser import FunctionNode, parse, Node, ConstantNode
from inequality.Relationship import Relationship, Relation, ConditionalRelationship


def subtraction(cond_rel: ConditionalRelationship, operand: Node, cache: ExplosionCache) -> set[ConditionalRelationship]:
    operand, _ = simplify(operand, cache)  # this is necessary because it should remove unused variables
    options = set()
    rel = cond_rel.relationship
    conds = cond_rel.conditions
    _lhs = FunctionNode('-', [rel.lhs, operand])
    _rhs = FunctionNode('-', [rel.rhs, operand])
    _rel = Relationship(_lhs, rel.relation, _rhs)
    options.add(ConditionalRelationship(_rel, conds))
    return options


if __name__ == '__main__':
    rel = ConditionalRelationship(
        Relationship(parse('x-2'), Relation.LT, parse('0')),
        frozenset()
    )
    options = subtraction(rel, parse('x+x+x'), ExplosionCache())
    for rel in options:
        print(f'{rel}')
