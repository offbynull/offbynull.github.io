`{bm-disable-all}`[arithmetic_code/FractionNumber.py](arithmetic_code/FractionNumber.py) (lines 96 to 124):`{bm-enable-all}`

```python
@staticmethod
@log_decorator
def common_denominator_naive(lhs: FractionNumber, rhs: FractionNumber) -> (FractionNumber, FractionNumber):
    # Sign is only kept on the numerator, not the denominator
    log(f'Getting {lhs} and {rhs} to common denominator equivalent fractions')
    if lhs._denominator != rhs._denominator:
        log_indent()

        log(f'Calculating common denominator...')
        common_denominator = rhs._denominator * lhs._denominator
        log(f'{common_denominator}')

        log(f'Calculating numerator for LHS ({lhs})...')
        lhs_numerator = lhs._numerator * rhs._denominator
        log(f'{lhs_numerator}')

        log(f'Calculating numerator for RHS ({rhs})...')
        rhs_numerator = rhs._numerator * lhs._denominator
        log(f'{rhs_numerator}')

        log_unindent()

        lhs_equiv = FractionNumber(lhs_numerator, common_denominator)
        rhs_equiv = FractionNumber(rhs_numerator, common_denominator)
        log(f'Result: {lhs} -> {lhs_equiv}, {rhs} -> {rhs_equiv}')
        return lhs_equiv, rhs_equiv
    else:
        log(f'Fractions already have a common denominator')
        return lhs, rhs
```