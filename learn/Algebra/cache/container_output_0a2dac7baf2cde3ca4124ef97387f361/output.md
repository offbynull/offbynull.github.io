`{bm-disable-all}`[arithmetic_code/Factor.py](arithmetic_code/Factor.py) (lines 104 to 124):`{bm-enable-all}`

```python
@log_decorator
def factor_tree(num: int) -> FactorTreeNode:
    log(f'Creating factor tree for {num}...')

    factors = factor_fastest(num)

    # remove factor pairs that can't used in factor true: (1, num) or (num, 1)
    factors = set([f for f in factors if f != 1 and f != num])

    ret = FactorTreeNode()
    if len(factors) == 0:
        ret.value = num
        log(f'Cannot factor {num} is prime -- resulting tree: {ret}')
    else:
        factor1 = next(iter(factors))
        factor2 = num // factor1
        ret.value = num
        ret.left = factor_tree(factor1)
        ret.right = factor_tree(factor2)
        log(f'Factored {num} to {factor1} and {factor2} -- resulting tree: {ret}')
    return ret
```