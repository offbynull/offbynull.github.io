`{bm-disable-all}`[arithmetic_code/expression/properties/RatioAdditionProperties.py](arithmetic_code/expression/properties/RatioAdditionProperties.py) (lines 69 to 76):`{bm-enable-all}`

```python
def inverse(n: Node):
    if not isinstance(n, FunctionNode):
        return set()
    if n.op == '+':
        if (isinstance(n.args[0], ConstantNode) and n.args[1] == -n.args[0])\
                or n.args[1] == FunctionNode('*', [ConstantNode(-1), n.args[0]]):
            return {ConstantNode(0)}
    return set()
```