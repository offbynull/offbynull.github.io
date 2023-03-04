`{bm-disable-all}`[arithmetic_code/expression/properties/RatioSubtractionProperties.py](arithmetic_code/expression/properties/RatioSubtractionProperties.py) (lines 35 to 67):`{bm-enable-all}`

```python
def combine(n: Node):
    if not isinstance(n, FunctionNode):
        return set()
    if n.op == '-':
        l_arg, r_arg = n.args
        ret = FunctionNode('/', [
            FunctionNode(
                '-',
                [
                    FunctionNode('*', [top(l_arg), bottom(r_arg)]),
                    FunctionNode('*', [top(r_arg), bottom(l_arg)])
                ]
            ),
            FunctionNode('*', [bottom(l_arg), bottom(r_arg)])
        ])
        return {ret}
    return set()


def uncombine(n: Node):
    if not isinstance(n, FunctionNode):
        return set()
    fn_top = top(n)
    fn_bottom = bottom(n)
    if isinstance(fn_top, FunctionNode) and fn_top.op == '-':
        l_arg = fn_top.args[0]
        r_arg = fn_top.args[1]
        ret = FunctionNode('-', [
            FunctionNode('/', [l_arg, fn_bottom]),
            FunctionNode('/', [r_arg, fn_bottom])
        ])
        return {ret}
    return set()
```