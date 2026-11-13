`{bm-disable-all}`[arithmetic_code/expression/properties/ArithmeticConversions.py](arithmetic_code/expression/properties/ArithmeticConversions.py) (lines 57 to 92):`{bm-enable-all}`

```python
def add_to_mul(n: Node):
    if isinstance(n, FunctionNode) and n.op == '+':
        lhs, rhs = n.args
        lhs_const, lhs_factor = _split_out_multiplication_constant(lhs)
        rhs_const, rhs_factor = _split_out_multiplication_constant(rhs)
        if lhs_const is None or lhs_factor is None or rhs_const is None or rhs_factor is None:
            return set()
        if lhs_factor != rhs_factor:
            return set()
        _n = FunctionNode('*', [lhs_const + rhs_const, lhs_factor])
        return {_n}
    return set()


def mul_to_add(n: Node):
    if isinstance(n, FunctionNode) and n.op == '*':
        const, factor = _split_out_multiplication_constant(n)
        if factor is None or const is None:
            return set()
        if const > 0:
            _n = factor
            while const > 1:
                _n = FunctionNode('+', [factor, _n])
                const = const - 1
            return {_n}
    return set()


def _split_out_multiplication_constant(a: Node):
    if isinstance(a, ConstantNode) or isinstance(a, VariableNode):
        return ConstantNode(1), a
    elif isinstance(a, FunctionNode) and a.op == '*' and isinstance(a.args[0], ConstantNode):
        a_lhs, a_rhs = a.args
        return a_lhs, a_rhs
    return None, None
```