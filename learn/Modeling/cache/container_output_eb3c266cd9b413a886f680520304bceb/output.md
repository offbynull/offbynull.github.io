```python
def multinomial_coefficient(exp: int, group_counts: list[int]) -> int:
    assert sum(group_counts) == exp
    num = factorial(exp)
    denom = 1
    for g in group_counts:
        denom *= factorial(g)
    return num // denom


def multinomial_coefficients(exp: int, nomial_count: int) -> list[int]:
    ret = []
    for term_exponents in product(range(exp+1), repeat=nomial_count):
        term_exponents = list(term_exponents)
        if sum(term_exponents) != exp:
            continue
        c = multinomial_coefficient(exp, term_exponents)
        ret.append(c)
    return ret
```