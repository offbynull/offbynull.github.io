`{bm-disable-all}`[arithmetic_code/Factor.py](arithmetic_code/Factor.py) (lines 56 to 79):`{bm-enable-all}`

```python
@log_decorator
def factor_fastest(num: WholeNumber) -> Set[WholeNumber]:
    log(f'Factoring {num}...')
    log_indent()

    factors: Set[WholeNumber] = set()
    for factor1 in WholeNumber.range(WholeNumber.from_int(1), num, end_inclusive=True):
        log(f'Test if {factor1} is a factor...')
        factor2, remainder = num / factor1
        if remainder == WholeNumber.from_int(0):
            factors.add(factor1)
            factors.add(factor2)
            log(f'Yes: ({factor1} and {factor2} are factors)')
        else:
            log(f'No')

        if factor2 <= factor1:
            break

    log_unindent()
    log(f'{factors}')

    return factors
```