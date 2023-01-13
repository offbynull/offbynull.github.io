`{bm-disable-all}`[arithmetic_code/FractionNumber.py](arithmetic_code/FractionNumber.py) (lines 222 to 231):`{bm-enable-all}`

```python
@log_decorator
def __truediv__(lhs: FractionNumber, rhs: FractionNumber) -> FractionNumber:
    # Sign is only kept on the numerator, not the denominator
    log(f'Dividing {lhs} and {rhs}')

    res = FractionNumber(lhs._numerator * rhs._denominator, lhs._denominator * rhs._numerator)
    log(f'Result: {res}')

    return res
```