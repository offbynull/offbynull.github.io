`{bm-disable-all}`[arithmetic_code/expression/properties/DistributiveProperty.py](arithmetic_code/expression/properties/DistributiveProperty.py) (lines 14 to 48):`{bm-enable-all}`

```python
def distributive(n: Node):
    if not isinstance(n, FunctionNode) or n.op != '*':
        return set()
    lhs = n.args[0]
    rhs = n.args[1]
    if isinstance(rhs, FunctionNode) and rhs.op == '+':
        _n = FunctionNode(
            '+',
            [
                FunctionNode('*', [lhs, rhs.args[0]]),
                FunctionNode('*', [lhs, rhs.args[1]]),
            ]
        )
        return {_n}
    return set()


def undistributive_basic(n: Node):
    if not isinstance(n, FunctionNode) or n.op not in '+':
        return set()
    lhs = n.args[0]
    rhs = n.args[1]
    if isinstance(lhs, FunctionNode) and lhs.op == '*'\
            and isinstance(rhs, FunctionNode) and rhs.op == '*'\
            and lhs.args[0] == rhs.args[0]:
        _n = FunctionNode(
            '*',
            [
                lhs.args[0],
                FunctionNode('+', [lhs.args[1], rhs.args[1]])
            ]
        )
        return {_n}
    return set()
```