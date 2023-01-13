`{bm-disable-all}`[arithmetic_code/FractionNumber.py](arithmetic_code/FractionNumber.py) (lines 182 to 198):`{bm-enable-all}`

```python
@log_decorator
def __sub__(lhs: FractionNumber, rhs: FractionNumber) -> FractionNumber:
    # Sign is only kept on the numerator, not the denominator
    log(f'Subtracting {lhs} and {rhs}...')
    log(f'Converting {lhs} and {rhs} to equivalent fractions with least common denominator...')

    log(f'Converting {lhs} and {rhs} to equivalent fractions with least common denominator...')
    lhs, rhs = FractionNumber.common_denominator_lcm(lhs, rhs)
    log(f'Equivalent fractions: {lhs} and {rhs}')
    log(f'Subtracting numerators of {lhs} and {rhs}...')
    res = FractionNumber(lhs._numerator - rhs._numerator, lhs._denominator)

    log_unindent()
    log(f'Result: {res}')

    return res
```