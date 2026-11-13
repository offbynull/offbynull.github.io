`{bm-disable-all}`[arithmetic_code/relation/properties/LessThanOrEqualProperties.py](arithmetic_code/relation/properties/LessThanOrEqualProperties.py) (lines 17 to 23):`{bm-enable-all}`

```python
def addition(rel: Relation, operand: Node, cache: ExplosionCache) -> set[RelationWithDomain]:
    if rel.op == '<=':
        _lhs = FunctionNode('+', [rel.lhs, operand])
        _rhs = FunctionNode('+', [rel.rhs, operand])
        return {RelationWithDomain.create(rel.op, _lhs, _rhs)}
    return set()
```