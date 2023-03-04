`{bm-disable-all}`[arithmetic_code/expression/properties/RatioDivisionProperties.py](arithmetic_code/expression/properties/RatioDivisionProperties.py) (lines 36 to 42):`{bm-enable-all}`

```python
def zero(n: Node):
    if isinstance(n, FunctionNode) and n.op == '/':
        l_arg = n.args[0]
        if l_arg == 0:
            return {ConstantNode(0)}
    return set()
```