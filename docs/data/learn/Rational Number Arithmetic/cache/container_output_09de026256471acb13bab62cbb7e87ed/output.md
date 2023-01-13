`{bm-disable-all}`[arithmetic_code/DecimalNumber.py](arithmetic_code/DecimalNumber.py) (lines 215 to 247):`{bm-enable-all}`

```python
@log_decorator
def as_fraction(self: DecimalNumber) -> FractionNumber:
    log(f'Converting {self} to fraction number...')
    log_indent()

    log(f'Determining denominator based on length of fractional portion ({self.fractional})...')
    denom = IntegerNumber.from_str('1' + '0' * len(self.fractional.digits))
    log(f'{denom}')

    log(f'Converting fractional portion ({self.fractional} to fraction...')
    fractional_fraction = FractionNumber(
        IntegerNumber.from_str(str(self.fractional)),
        denom
    )
    log(f'{fractional_fraction}')

    log(f'Converting whole portion ({self.whole}) to fraction...')
    whole_fraction = FractionNumber.from_whole(self.whole)
    log(f'{whole_fraction}')

    log(f'Adding ({whole_fraction}) to ({fractional_fraction})...')
    fraction = whole_fraction + fractional_fraction
    log(f'{fraction}')

    log(f'Applying sign of ({self.sign}) to {fraction}...')
    if self.sign == Sign.NEGATIVE:
        fraction = fraction * FractionNumber.from_str("-1/1")  # make sign negative
    log(f'{fraction}')

    log_unindent()

    return fraction
```