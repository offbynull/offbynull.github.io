`{bm-disable-all}`[arithmetic_code/expression/properties/ArithmeticConversions.py](arithmetic_code/expression/properties/ArithmeticConversions.py) (lines 96 to 131):`{bm-enable-all}`

```python
def mul_to_exp(n: FunctionNode):
    if isinstance(n, FunctionNode) and n.op == '*':
        lhs, rhs = n.args
        lhs_base, lhs_const = _split_out_exponent_constant(lhs)
        rhs_base, rhs_const = _split_out_exponent_constant(rhs)
        if lhs_const is None or lhs_base is None or rhs_const is None or rhs_base is None:
            return set()
        if lhs_base != rhs_base:
            return set()
        _n = FunctionNode('^', [lhs_base, lhs_const + rhs_const])
        return {_n}
    return set()


def exp_to_mul(n: FunctionNode):
    if isinstance(n, FunctionNode) and n.op == '^':
        base, exp = _split_out_exponent_constant(n)
        if base is None or exp is None:
            return set()
        if exp > 0:
            _n = base
            while exp > 1:
                _n = FunctionNode('*', [base, _n])
                exp = exp - 1
            return {_n}
    return set()


def _split_out_exponent_constant(a: Node):
    if isinstance(a, ConstantNode) or isinstance(a, VariableNode):
        return a, ConstantNode(1)
    elif isinstance(a, FunctionNode) and a.op == '^' and isinstance(a.args[1], ConstantNode):
        a_lhs, a_rhs = a.args
        return a_lhs, a_rhs
    return None, None
```