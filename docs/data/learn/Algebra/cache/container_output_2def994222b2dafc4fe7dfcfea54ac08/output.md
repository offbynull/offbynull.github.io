`{bm-disable-all}`[arithmetic_code/expression/properties/RatioMultiplicationProperties.py](arithmetic_code/expression/properties/RatioMultiplicationProperties.py) (lines 101 to 131):`{bm-enable-all}`

```python
def combine(n: Node):
    if not isinstance(n, FunctionNode):
        return set()
    if n.op == '*':
        l_arg, r_arg = n.args
        if isinstance(l_arg, ConstantNode) and isinstance(r_arg, ConstantNode):
            return {ConstantNode(l_arg.value * r_arg.value)}
        ret = FunctionNode('/', [
            FunctionNode('*', [top(l_arg), top(r_arg)]),
            FunctionNode('*', [bottom(l_arg), bottom(r_arg)])
        ])
        return {ret}
    return set()


def uncombine(n: Node):
    if not isinstance(n, FunctionNode):
        return set()
    n_top = top(n)
    n_bottom = bottom(n)
    if isinstance(n_top, FunctionNode) and n_top.op == '*':
        l_arg = n_top.args[0]
        r_arg = n_top.args[1]
        ret = {
            FunctionNode('*', [
                FunctionNode('/', [l_arg, n_bottom]),
                FunctionNode('/', [r_arg, ConstantNode(1)])
            ])
        }
        return ret
    return set()
```