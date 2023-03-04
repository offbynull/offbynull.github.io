`{bm-disable-all}`[arithmetic_code/expression/properties/RatioAdditionProperties.py](arithmetic_code/expression/properties/RatioAdditionProperties.py) (lines 14 to 24):`{bm-enable-all}`

```python
def commutative(n: Node):
    if not isinstance(n, FunctionNode):
        return set()
    variations = set()
    if n.op == '+':
        _n = FunctionNode(
            n.op,
            n.args[::-1]
        )
        variations.add(_n)
    return variations
```