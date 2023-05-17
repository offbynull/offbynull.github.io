```python
def binomial_coefficients(exp: int) -> list[int]:
    ret = []
    for r in range(exp + 1):
        c = count_combinations(exp, r)
        ret.append(c)
    return ret
```