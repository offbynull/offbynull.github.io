from expression.Exploder import ExplosionCache, simplify
from expression.parser.Parser import FunctionNode, parse, Node, VariableNode, ConstantNode
from inequality.Relationship import Relationship, Relation, ConditionalRelationship


def multiplication(cond_rel: ConditionalRelationship, operand: Node, cache: ExplosionCache) -> set[ConditionalRelationship]:
    operand, _ = simplify(operand, cache)  # this is necessary because it should remove unused variables
    options = set()
    rel = cond_rel.relationship
    conds = cond_rel.conditions
    _lhs = FunctionNode('*', [rel.lhs, operand])
    _rhs = FunctionNode('*', [rel.rhs, operand])
    if _has_variable(operand):
        # if operand is > 0, keep relation
        _rel = Relationship(_lhs, rel.relation, _rhs)
        _conds = conds | {Relationship(operand, Relation.GT, ConstantNode(0))}
        options.add(ConditionalRelationship(_rel, _conds))
        # if operand is < 0, swap relation
        _rel = Relationship(_lhs, rel.relation.swap(), _rhs)
        _conds = conds | {Relationship(operand, Relation.LT, ConstantNode(0))}
        options.add(ConditionalRelationship(_rel, _conds))
        # if operand is = 0 (anything multiplied by 0 is 0)
        _rel = Relationship(_lhs, Relation.EQ, _rhs)
        _conds = conds | {Relationship(operand, Relation.EQ, ConstantNode(0))}
        options.add(ConditionalRelationship(_rel, _conds))
    else:
        sign = _constant_sign(operand)
        match sign:
            case '+':
                _rel = Relationship(_lhs, rel.relation, _rhs)  # keep relation if pos
                options.add(ConditionalRelationship(_rel, conds))
            case '-':
                _rel = Relationship(_lhs, rel.relation.swap(), _rhs)  # swap relation if neg
                options.add(ConditionalRelationship(_rel, conds))
            case '0':
                _rel = Relationship(_lhs, Relation.EQ, _rhs)  # multiply by 0 means both sides equal to 0
                options.add(ConditionalRelationship(_rel, conds))
            case _:
                raise ValueError('This should never happen')
    return options


def _has_variable(n: Node):
    if isinstance(n, VariableNode):
        return True
    elif isinstance(n, ConstantNode):
        return False
    elif isinstance(n, FunctionNode):
        return any(_has_variable(_n) for _n in n.args)
    return ValueError('This should never happen')


def _constant_sign(n: Node):
    if isinstance(n, ConstantNode):
        if n > 0:
            sign = '+'
        elif n < 0:
            sign = '-'
        elif n == 0:
            sign = '0'
        else:
            raise ValueError('This should never happen')
    elif isinstance(n, FunctionNode) and n.op == '/' \
            and isinstance(n.args[0], ConstantNode) and isinstance(n.args[1], ConstantNode):
        if (n.args[0] > 0 and n.args[1] > 0) or (n.args[0] < 0 and n.args[1] < 0):
            sign = '+'  # pos/pos or neg/neg -- no swap in relation required
        elif n.args[1] == 0:
            raise ValueError('Division by zero is undefined')
        elif n.args[0] == 0:
            sign = None  # 0 numerator, meaning you're multiplying by zero
        else:
            sign = '-'  # pos/neg or neg/pos -- swap required
    else:
        raise ValueError(f'Unsure how to evaluate this: {n}')
    return sign


if __name__ == '__main__':
    rel = ConditionalRelationship(
        Relationship(parse('x-2'), Relation.LT, parse('0')),
        frozenset()
    )
    options = multiplication(rel, parse('x+x+x'), ExplosionCache())
    for rel in options:
        print(f'{rel}')
