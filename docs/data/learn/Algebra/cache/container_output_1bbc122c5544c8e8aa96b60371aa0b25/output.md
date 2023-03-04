`{bm-disable-all}`[arithmetic_code/expression/properties/RatioDivisionProperties.py](arithmetic_code/expression/properties/RatioDivisionProperties.py) (lines 74 to 103):`{bm-enable-all}`

```python
def combine(n: Node):
    if not isinstance(n, FunctionNode):
        return set()
    if n.op == '/':
        l_arg, r_arg = n.args
        ret = FunctionNode('/', [
            FunctionNode('*', [top(l_arg), bottom(r_arg)]),
            FunctionNode('*', [bottom(l_arg), top(r_arg)])
        ])
        return {ret}
    return set()


def uncombine(n: Node):
    if not isinstance(n, FunctionNode):
        return set()
    if n.op == '/':
        n_top = top(n)
        n_bottom = bottom(n)
        if not (isinstance(n_top, FunctionNode) and n_top.op == '*'
                and isinstance(n_bottom, FunctionNode) and n_bottom.op == '*'):
            return set()
        l_top, r_top = n_top.args
        l_bottom, r_bottom = n_bottom.args
        ret = FunctionNode('/', [
            FunctionNode('/', [l_top, l_bottom]),
            FunctionNode('/', [r_bottom, r_top])
        ])
        return {ret}
    return set()
```