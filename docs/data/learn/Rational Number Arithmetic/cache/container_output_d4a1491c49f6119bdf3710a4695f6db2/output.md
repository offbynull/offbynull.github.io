`{bm-disable-all}`[arithmetic_code/IntegerNumber.py](arithmetic_code/IntegerNumber.py) (lines 85 to 123):`{bm-enable-all}`

```python
@log_decorator
def __sub__(lhs: IntegerNumber, rhs: IntegerNumber) -> IntegerNumber:
    log(f'Subtracting {lhs} and {rhs}')
    log_indent()

    def determine_sign(magnitude: WholeNumber, default_sign: Sign) -> Sign:
        if magnitude == WholeNumber.from_int(0):
            return None
        else:
            return default_sign

    def flip_sign(sign: Sign) -> Sign:
        if sign == Sign.POSITIVE:
            return Sign.NEGATIVE
        elif sign == Sign.NEGATIVE:
            return Sign.POSITIVE

    if lhs.sign is None:  # sign of None is only when magnitude is 0,  0 - a = -a
        sign = flip_sign(rhs.sign)
        magnitude = rhs.magnitude
    elif rhs.sign is None:  # sign of None is only when magnitude is 0,  a - 0 = a
        sign = lhs.sign
        magnitude = lhs.magnitude
    elif lhs.sign == rhs.sign:
        if rhs.magnitude >= lhs.magnitude:
            magnitude = rhs.magnitude - lhs.magnitude
            sign = determine_sign(magnitude, flip_sign(lhs.sign))
        else:
            magnitude = lhs.magnitude - rhs.magnitude
            sign = determine_sign(magnitude, lhs.sign)
    elif lhs.sign != rhs.sign:
        magnitude = lhs.magnitude + rhs.magnitude
        sign = determine_sign(magnitude, lhs.sign)

    log_unindent()
    log(f'sign: {sign}, magnitude: {magnitude}')

    return IntegerNumber(sign, magnitude)
```