`{bm-disable-all}`[arithmetic_code/expression/properties/RatioMultiplicationProperties.py](arithmetic_code/expression/properties/RatioMultiplicationProperties.py) (lines 60 to 65):`{bm-enable-all}`

```python
def identity(n: Node):
    if not isinstance(n, FunctionNode):
        return set()
    if n.op == '*' and n.args[1] == 1:
        return {n.args[0]}
    return set()
```