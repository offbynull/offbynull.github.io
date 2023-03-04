`{bm-disable-all}`[arithmetic_code/expression/properties/ArithmeticConversions.py](arithmetic_code/expression/properties/ArithmeticConversions.py) (lines 34 to 51):`{bm-enable-all}`

```python
def sub_to_add(n: FunctionNode):
    if isinstance(n, FunctionNode) and n.op == '-':
        lhs = n.args[0]
        rhs = n.args[1]
        rhs_negated = FunctionNode('*', [ConstantNode(-1), rhs])
        _n = FunctionNode('+', [lhs, rhs_negated])
        return {_n}
    return set()


def add_to_sub(n: FunctionNode):
    if isinstance(n, FunctionNode) and n.op == '+':
        lhs = n.args[0]
        rhs = n.args[1]
        rhs_negated = FunctionNode('*', [ConstantNode(-1), rhs])
        _n = FunctionNode('-', [lhs, rhs_negated])
        return {_n}
    return set()
```