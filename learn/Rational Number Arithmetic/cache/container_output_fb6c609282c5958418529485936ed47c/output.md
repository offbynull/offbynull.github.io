`{bm-disable-all}`[arithmetic_code/FractionNumber.py](arithmetic_code/FractionNumber.py) (lines 201 to 219):`{bm-enable-all}`

```python
@log_decorator
def __mul__(lhs: FractionNumber, rhs: FractionNumber) -> FractionNumber:
    # Sign is only kept on the numerator, not the denominator
    log(f'Multiplying {lhs} and {rhs}')
    log_indent()

    log(f'Multiplying numerators {lhs._numerator} and {rhs._numerator}...')
    numerator = lhs._numerator * rhs._numerator

    log(f'Multiplying denominators {lhs._denominator} and {rhs._denominator}...')
    denominator = lhs._denominator * rhs._denominator

    res = FractionNumber(numerator, denominator)

    log_unindent()
    log(f'Result: {res}')

    return res
```