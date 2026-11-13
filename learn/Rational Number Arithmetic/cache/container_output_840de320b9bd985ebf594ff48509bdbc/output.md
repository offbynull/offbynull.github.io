`{bm-disable-all}`[arithmetic_code/FractionNumber.py](arithmetic_code/FractionNumber.py) (lines 246 to 282):`{bm-enable-all}`

```python
@log_decorator
def simplify(self: FractionNumber) -> FractionNumber:
    # Sign is on the numerator
    log(f'Simplifying {self}...')
    log_indent()

    log(f'Calculating GCD for ({self._numerator.magnitude}) and ({self._denominator.magnitude})...')
    gcd = gcd_euclid(self._numerator.magnitude, self._denominator.magnitude)
    log(f'GCD is {gcd}')

    log(f'Dividing numerator ({self._numerator.magnitude}) by {gcd}...')
    new_num, _ = self._numerator.magnitude / gcd
    log(f'New numerator is {new_num}...')

    log(f'Dividing denominator ({self._denominator.magnitude}) by {gcd}...')
    new_den, _ = self._denominator.magnitude / gcd
    log(f'New numerator is {new_den}...')

    # Sign of fraction is on the numerator
    if self.sign == Sign.NEGATIVE:  # if original was negative, so will the simplified
        res = FractionNumber(
            IntegerNumber(Sign.NEGATIVE, new_num),
            IntegerNumber(Sign.POSITIVE, new_den))
    elif self.sign == Sign.POSITIVE:  # if original was positive, so will the simplified
        res = FractionNumber(
            IntegerNumber(Sign.POSITIVE, new_num),
            IntegerNumber(Sign.POSITIVE, new_den))
    else:  # if original was 0 (no sign), so will the simplified
        res = FractionNumber(
            IntegerNumber(None, new_num),
            IntegerNumber(Sign.POSITIVE, new_den))

    log_unindent()
    log(f'{self} simplified to: {res}')

    return res
```