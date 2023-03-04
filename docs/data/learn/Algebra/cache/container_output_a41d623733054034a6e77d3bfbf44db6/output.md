`{bm-disable-all}`[arithmetic_code/expression/properties/RatioMultiplicationProperties.py](arithmetic_code/expression/properties/RatioMultiplicationProperties.py) (lines 70 to 76):`{bm-enable-all}`

```python
def inverse(n: Node):
    if not isinstance(n, FunctionNode):
        return set()
    if n.op == '*':
        if n.args[1] == FunctionNode('/', [ConstantNode(1), n.args[0]]):
            return {ConstantNode(1)}
    return set()
```