`{bm-disable-all}`[arithmetic_code/expression/properties/RatioSubtractionProperties.py](arithmetic_code/expression/properties/RatioSubtractionProperties.py) (lines 25 to 31):`{bm-enable-all}`

```python
def inverse(n: Node):
    if not isinstance(n, FunctionNode):
        return set()
    if n.op == '-':
        if n.args[0] == n.args[1]:
            return {ConstantNode(0)}
    return set()
```