`{bm-disable-all}`[arithmetic_code/relation/properties/NotEqualProperties.py](arithmetic_code/relation/properties/NotEqualProperties.py) (lines 51 to 61):`{bm-enable-all}`

```python
def division(rel: Relation, operand: Node, cache: ExplosionCache) -> set[RelationWithDomain]:
    if rel.op == '!=':
        operand, _ = simplify(operand, cache)
        if operand == 0:
            return {RelationWithDomain.create('=', ConstantNode(0), ConstantNode(0))}
        else:
            _lhs = FunctionNode('/', [rel.lhs, operand])
            _rhs = FunctionNode('/', [rel.rhs, operand])
            return {RelationWithDomain.create(rel.op, _lhs, _rhs, {Relation('!=', operand, ConstantNode(0))})}
    return set()
```