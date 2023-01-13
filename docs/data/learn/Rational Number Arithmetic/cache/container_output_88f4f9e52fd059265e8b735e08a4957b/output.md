`{bm-disable-all}`[arithmetic_code/FractionNumber.py](arithmetic_code/FractionNumber.py) (lines 234 to 243):`{bm-enable-all}`

```python
@log_decorator
def reciprocal(self: FractionNumber) -> FractionNumber:
    # Sign is on the numerator
    log(f'Getting reciprocal of {self}')

    res = FractionNumber(self._denominator, self._numerator)
    log(f'Result: {res}')

    return res
```