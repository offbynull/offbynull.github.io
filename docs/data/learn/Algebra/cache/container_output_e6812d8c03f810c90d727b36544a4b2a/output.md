`{bm-disable-all}`[arithmetic_code/expression/properties/ArithmeticConversions.py](arithmetic_code/expression/properties/ArithmeticConversions.py) (lines 14 to 29):`{bm-enable-all}`

```python
def prime_factors(n: Node):
    if not isinstance(n, ConstantNode):
        return set()
    negative = n < 0
    if negative:
        n = -n
    if n in {0, 1, -1}:
        return set()
    factors = factor_tree(n.value.numerator).get_prime_factors()
    last = ConstantNode(factors.pop())
    while factors:
        new = ConstantNode(factors.pop())
        last = FunctionNode('*', [last, new])
    if negative:
        last = FunctionNode('*', [ConstantNode(-1), last])
    return {last}
```