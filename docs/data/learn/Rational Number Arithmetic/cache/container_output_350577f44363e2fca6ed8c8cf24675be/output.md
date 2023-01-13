`{bm-disable-all}`[arithmetic_code/IntegerNumber.py](arithmetic_code/IntegerNumber.py) (lines 232 to 263):`{bm-enable-all}`

```python
@log_decorator
def __lt__(self: IntegerNumber, other: IntegerNumber) -> bool:
    log(f'Less than testing {self} and {other}...')
    log_indent()

    self_sign = self.sign
    if self_sign is None:  # assume 0 is a positive -- it simplifies logic below
        self_sign = Sign.POSITIVE

    other_sign = other.sign
    if other_sign is None:  # assume 0 is a positive -- it simplifies logic below
        other_sign = Sign.POSITIVE

    if self_sign == Sign.POSITIVE and other_sign == Sign.POSITIVE:
        log(f'{self.sign} < {other.sign}: Applying whole number less than...')
        ret = self.magnitude < other.magnitude
    elif self_sign == Sign.NEGATIVE and other_sign == Sign.NEGATIVE:
        log(f'{self.sign} < {other.sign}: Turning positive and applying whole number greater than...')
        ret = self.magnitude > other.magnitude
    elif self_sign == Sign.POSITIVE and other_sign == Sign.NEGATIVE:
        log(f'{self.sign} < {other.sign}:: Different signs -- number being tested is positive...')
        ret = False
    elif self_sign == Sign.NEGATIVE and other_sign == Sign.POSITIVE:
        log(f'{self.sign} < {other.sign}: Different signs -- number being tested is negative...')
        ret = True
    log(f'{ret}')

    log_unindent()
    log(f'{ret}')

    return ret
```