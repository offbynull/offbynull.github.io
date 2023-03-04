from expression.Exploder import ExplosionCache, simplify
from expression.Node import Node
from expression.parser.Parser import FunctionNode, parse, VariableNode, ConstantNode
from relation.Relation import Relation, RelationWithDomain, opposite


def division(rel_with_dom: RelationWithDomain, operand: Node, cache: ExplosionCache) -> set[RelationWithDomain]:
    operand, _ = simplify(operand, cache)  # this is necessary because it should remove unused variables
    options = set()
    rel = rel_with_dom.relation
    doms = rel_with_dom.domains
    _lhs = FunctionNode('/', [rel.lhs, operand])
    _rhs = FunctionNode('/', [rel.rhs, operand])
    if _has_variable(operand):
        # if operand is > 0, keep relation
        _rel = Relation(rel.op, _lhs, _rhs)
        _doms = doms | {Relation('>', operand, ConstantNode(0))}
        options.add(RelationWithDomain(_rel, _doms))
        # if operand is < 0, swap relation
        _rel = Relation(opposite(rel.op), _lhs, _rhs)
        _doms = doms | {Relation('<', operand, ConstantNode(0))}
        options.add(RelationWithDomain(_rel, _doms))
        # if operand is = 0, operation can't exist (anything divided by 0 is not allowed)
    else:
        sign = _constant_sign(operand)
        match sign:
            case '+':
                _rel = Relation(rel.op, _lhs, _rhs)  # keep relation if pos
                options.add(RelationWithDomain(_rel, doms))
            case '-':
                _rel = Relation(opposite(rel.op), _lhs, _rhs)  # swap relation if neg
                options.add(RelationWithDomain(_rel, doms))
            case '0':
                ...  # divide by 0, operation can't exist (anything divided by 0 is not allowed)
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
    rel = RelationWithDomain(
        Relation('<', parse('x-2'), parse('0')),
        frozenset()
    )
    options = division(rel, parse('x+x+x'), ExplosionCache())
    for rel in options:
        print(f'{rel}')
