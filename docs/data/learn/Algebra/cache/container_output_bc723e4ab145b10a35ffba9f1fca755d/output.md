`{bm-disable-all}`[arithmetic_code/expression/properties/RatioSubtractionProperties.py](arithmetic_code/expression/properties/RatioSubtractionProperties.py) (lines 15 to 20):`{bm-enable-all}`

```python
def identity(n: Node):
    if not isinstance(n, FunctionNode):
        return set()
    if n.op == '-' and n.args[1] == 0:
        return {n.args[0]}
    return set()
```