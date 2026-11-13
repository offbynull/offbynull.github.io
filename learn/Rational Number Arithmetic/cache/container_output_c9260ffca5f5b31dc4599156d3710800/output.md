`{bm-disable-all}`[arithmetic_code/FractionNumber.py](arithmetic_code/FractionNumber.py) (lines 382 to 417):`{bm-enable-all}`

```python
@log_decorator
def __gt__(lhs: FractionNumber, rhs: FractionNumber) -> bool:
    log(f'Greater than testing {lhs} and {rhs}...')
    log_indent()

    # Sign is only kept on the numerator, not the denominator
    log(f'Checking if denominators are the same...')
    if lhs._denominator != rhs._denominator:
        log(f'Not same -- finding equivalent fractions with common denominator...')
        log_indent()

        log(f'Calculating common denominator...')
        denominator = rhs._denominator * lhs._denominator
        log(f'{denominator}')

        log(f'Scaling numerator for {lhs} so denominator becomes {denominator}...')
        lhs_numerator = lhs._numerator * rhs._denominator
        log(f'Numerator: {lhs_numerator} Denominator: {denominator}')

        log(f'Scaling numerator for {rhs} so denominator becomes {denominator}...')
        rhs_numerator = rhs._numerator * lhs._denominator
        log(f'Numerator: {rhs_numerator} Denominator: {denominator}')

        log_unindent()
    else:
        log(f'Same')
        lhs_numerator = lhs._numerator
        rhs_numerator = rhs._numerator
        denominator = rhs._denominator

    log(f'Testing {lhs_numerator} > {rhs_numerator}...')
    ret = lhs_numerator > rhs_numerator
    log(f'{ret}')

    return ret
```