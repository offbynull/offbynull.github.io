`{bm-disable-all}`[arithmetic_code/relation/properties/EqualProperties.py](arithmetic_code/relation/properties/EqualProperties.py) (lines 44 to 57):`{bm-enable-all}`

```python
def division(rel: Relation, operand: Node, cache: ExplosionCache) -> set[RelationWithDomain]:
    if rel.op == '=':
        operand, _ = simplify(operand, cache)
        _lhs = FunctionNode('/', [rel.lhs, operand])
        _rhs = FunctionNode('/', [rel.rhs, operand])
        if isinstance(operand, ConstantNode):
            if operand == 0:
                return set()  # operand of 0 not allowed
            else:
                return {RelationWithDomain.create(rel.op, _lhs, _rhs)}
        else:
            return {RelationWithDomain.create(rel.op, _lhs, _rhs, {Relation('!=', operand, ConstantNode(0))})}
    return set()
```