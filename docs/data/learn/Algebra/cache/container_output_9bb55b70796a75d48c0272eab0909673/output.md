`{bm-disable-all}`[arithmetic_code/expression/properties/RatioMultiplicationProperties.py](arithmetic_code/expression/properties/RatioMultiplicationProperties.py) (lines 81 to 87):`{bm-enable-all}`

```python
def zero(n: Node):
    if isinstance(n, FunctionNode) and n.op == '*':
        r_arg = n.args[1]
        if r_arg == 0:
            return {ConstantNode(0)}
    return set()
```