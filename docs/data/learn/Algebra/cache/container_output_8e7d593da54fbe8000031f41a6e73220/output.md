`{bm-disable-all}`[arithmetic_code/expression/properties/EquivalentFractionProperty.py](arithmetic_code/expression/properties/EquivalentFractionProperty.py) (lines 19 to 36):`{bm-enable-all}`

```python
def equivalent_fraction_basic(n: Node):
    if not isinstance(n, FunctionNode):
        return set()
    if n.op == '/':
        l_arg = n.args[0]
        r_arg = n.args[1]
        if isinstance(l_arg, FunctionNode) and l_arg.op == '*' and isinstance(r_arg, FunctionNode) and r_arg.op == '*' \
                and l_arg.args[1] == r_arg.args[1]:
            _n = FunctionNode(
                '*',
                [
                    FunctionNode('/', [l_arg.args[0], r_arg.args[0]]),
                    FunctionNode('/', [l_arg.args[1], r_arg.args[1]])
                ]
            )
            return {_n}
    return set()
```