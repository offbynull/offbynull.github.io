`{bm-disable-all}`[arithmetic_code/expression/properties/RatioDivisionProperties.py](arithmetic_code/expression/properties/RatioDivisionProperties.py) (lines 26 to 32):`{bm-enable-all}`

```python
def inverse(n: Node):
    if not isinstance(n, FunctionNode):
        return set()
    if n.op == '/':
        if n.args[0] == n.args[1] and n.args[1] != 0:
            return {ConstantNode(1)}
    return set()
```