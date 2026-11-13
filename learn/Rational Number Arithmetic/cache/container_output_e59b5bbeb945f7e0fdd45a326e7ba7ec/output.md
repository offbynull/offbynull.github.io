`{bm-disable-all}`[arithmetic_code/IntegerNumber.py](arithmetic_code/IntegerNumber.py) (lines 50 to 82):`{bm-enable-all}`

```python
@log_decorator
def __add__(lhs: IntegerNumber, rhs: IntegerNumber) -> IntegerNumber:
    log(f'Adding {lhs} and {rhs}')
    log_indent()

    def determine_sign(magnitude: WholeNumber, default_sign: Sign) -> Sign:
        if magnitude == WholeNumber.from_int(0):
            return None
        else:
            return default_sign

    if lhs.sign is None:  # sign of None is only when magnitude is 0,  0 + a = a
        sign = rhs.sign
        magnitude = rhs.magnitude
    elif rhs.sign is None:  # sign of None is only when magnitude is 0,  a + 0 = a
        sign = lhs.sign
        magnitude = lhs.magnitude
    elif lhs.sign == rhs.sign:
        magnitude = lhs.magnitude + rhs.magnitude
        sign = determine_sign(magnitude, lhs.sign)
    elif lhs.sign != rhs.sign:
        if rhs.magnitude >= lhs.magnitude:
            magnitude = rhs.magnitude - lhs.magnitude
            sign = determine_sign(magnitude, rhs.sign)
        else:
            magnitude = lhs.magnitude - rhs.magnitude
            sign = determine_sign(magnitude, lhs.sign)

    log_unindent()
    log(f'sign: {sign}, magnitude: {magnitude}')

    return IntegerNumber(sign, magnitude)
```