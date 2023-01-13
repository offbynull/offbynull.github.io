`{bm-disable-all}`[arithmetic_code/IntegerNumber.py](arithmetic_code/IntegerNumber.py) (lines 126 to 156):`{bm-enable-all}`

```python
@log_decorator
def __mul__(lhs: IntegerNumber, rhs: IntegerNumber) -> IntegerNumber:
    log(f'Multiplying {lhs} and {rhs}')
    log_indent()

    def determine_sign(magnitude: WholeNumber, default_sign: Sign) -> Sign:
        if magnitude == WholeNumber.from_int(0):
            return None
        else:
            return default_sign

    if lhs.sign is None:  # when sign isn't set, magnitude is always 0 -- 0 * a = 0
        sign = None
        magnitude = WholeNumber.from_int(0)
    elif rhs.sign is None:  # when sign isn't set, magnitude is always 0 -- a * 0 = 0
        sign = None
        magnitude = WholeNumber.from_int(0)
    elif (lhs.sign == Sign.POSITIVE and rhs.sign == Sign.POSITIVE) \
            or (lhs.sign == Sign.NEGATIVE and rhs.sign == Sign.NEGATIVE):
        magnitude = lhs.magnitude * rhs.magnitude
        sign = determine_sign(magnitude, Sign.POSITIVE)
    elif (lhs.sign == Sign.POSITIVE and rhs.sign == Sign.NEGATIVE) \
            or (lhs.sign == Sign.NEGATIVE and rhs.sign == Sign.POSITIVE):
        magnitude = lhs.magnitude * rhs.magnitude
        sign = determine_sign(magnitude, Sign.NEGATIVE)

    log_unindent()
    log(f'sign: {sign}, magnitude: {magnitude}')

    return IntegerNumber(sign, magnitude)
```