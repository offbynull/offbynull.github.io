`{bm-disable-all}`[arithmetic_code/expression/properties/RatioMultiplicationProperties.py](arithmetic_code/expression/properties/RatioMultiplicationProperties.py) (lines 30 to 55):`{bm-enable-all}`

```python
def associative(n: Node):
    if not isinstance(n, FunctionNode):
        return set()
    variations = set()
    if n.op == '*':
        l_arg = n.args[0]
        r_arg = n.args[1]
        if isinstance(l_arg, FunctionNode) and l_arg.op == n.op:
            _n = FunctionNode(
                n.op,
                [
                    l_arg.args[0],
                    FunctionNode(n.op, [l_arg.args[1], r_arg])
                ]
            )
            variations.add(_n)
        if isinstance(r_arg, FunctionNode) and r_arg.op == n.op:
            _n = FunctionNode(
                n.op,
                [
                    FunctionNode(n.op, [l_arg, r_arg.args[0]]),
                    r_arg.args[1]
                ]
            )
            variations.add(_n)
    return variations
```