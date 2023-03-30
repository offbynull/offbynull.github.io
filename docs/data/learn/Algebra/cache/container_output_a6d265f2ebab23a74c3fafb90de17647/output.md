`{bm-disable-all}`[arithmetic_code/relation/properties/LessThanProperties.py](arithmetic_code/relation/properties/LessThanProperties.py) (lines 35 to 66):`{bm-enable-all}`

```python
def multiplication(rel: Relation, operand: Node, cache: ExplosionCache) -> set[RelationWithDomain]:
    if rel.op == '<':
        operand, _ = simplify(operand, cache)
        if isinstance(operand, ConstantNode):
            if operand == 0:
                return set()  # operand of 0 not allowed
            else:
                _lhs = FunctionNode('*', [rel.lhs, operand])
                _rhs = FunctionNode('*', [rel.rhs, operand])
                if operand > 0:
                    return {RelationWithDomain.create(rel.op, _lhs, _rhs)}
                else:
                    return {RelationWithDomain.create(opposite(rel.op), _lhs, _rhs)}
        else:
            _lhs = FunctionNode('*', [rel.lhs, operand])
            _rhs = FunctionNode('*', [rel.rhs, operand])
            return {
                RelationWithDomain.create(
                    rel.op,
                    _lhs,
                    _rhs,
                    {Relation('>', operand, ConstantNode(0))}
                ),
                RelationWithDomain.create(
                    opposite(rel.op),
                    _lhs,
                    FunctionNode('*', [ConstantNode(-1), _rhs]),
                    {Relation('<', operand, ConstantNode(0))}
                )
            }
    return set()
```