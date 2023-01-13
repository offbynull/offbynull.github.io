`{bm-disable-all}`[arithmetic_code/Factor.py](arithmetic_code/Factor.py) (lines 8 to 28):`{bm-enable-all}`

```python
@log_decorator
def factor_naive(num: WholeNumber) -> Set[WholeNumber]:
    log(f'Factoring {num}...')
    log_indent()

    factors: Set[WholeNumber] = set()
    for factor1 in WholeNumber.range(WholeNumber.from_int(1), num, end_inclusive=True):
        for factor2 in WholeNumber.range(WholeNumber.from_int(1), num, end_inclusive=True):
            log(f'Testing if {factor1} and {factor2} are factors...')
            if factor1 * factor2 == num:
                factors.add(factor1)
                factors.add(factor2)
                log(f'Yes')
            else:
                log(f'No')

    log_unindent()
    log(f'{factors}')

    return factors
```