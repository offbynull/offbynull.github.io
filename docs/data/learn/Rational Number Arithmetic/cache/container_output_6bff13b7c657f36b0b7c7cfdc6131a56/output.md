`{bm-disable-all}`[arithmetic_code/IntegerNumber.py](arithmetic_code/IntegerNumber.py) (lines 159 to 192):`{bm-enable-all}`

```python
@log_decorator
def __truediv__(lhs: IntegerNumber, rhs: IntegerNumber) -> (IntegerNumber, IntegerNumber):
    log(f'Dividing {lhs} and {rhs}')
    log_indent()

    def determine_sign(magnitude: WholeNumber, default_sign: Sign) -> Sign:
        if magnitude == WholeNumber.from_int(0):
            return None
        else:
            return default_sign

    if lhs.sign is None:  # when sign isn't set, magnitude is always 0 -- 0 / a = 0
        (quotient_magnitude, remainder_magnitude) = lhs.magnitude / rhs.magnitude
        quotient_sign = None
        remainder_sign = None
    elif rhs.sign is None:  # when sign isn't set, magnitude is always 0 -- a / 0 = err
        raise Exception('Cannot divide by 0')
    elif (lhs.sign == Sign.POSITIVE and rhs.sign == Sign.POSITIVE) \
            or (lhs.sign == Sign.NEGATIVE and rhs.sign == Sign.NEGATIVE):
        (quotient_magnitude, remainder_magnitude) = lhs.magnitude / rhs.magnitude
        quotient_sign = determine_sign(quotient_magnitude, Sign.POSITIVE)
        remainder_sign = determine_sign(remainder_magnitude, Sign.POSITIVE)
    elif (lhs.sign == Sign.POSITIVE and rhs.sign == Sign.NEGATIVE) \
            or (lhs.sign == Sign.NEGATIVE and rhs.sign == Sign.POSITIVE):
        (quotient_magnitude, remainder_magnitude) = lhs.magnitude / rhs.magnitude
        quotient_sign = determine_sign(quotient_magnitude, Sign.NEGATIVE)
        remainder_sign = determine_sign(remainder_magnitude, Sign.NEGATIVE)

    log_unindent()
    log(f'QUOTIENT: sign: {quotient_sign}, magnitude: {quotient_magnitude}')
    log(f'REMAINDER: sign: {remainder_sign}, magnitude: {remainder_magnitude}')

    return IntegerNumber(quotient_sign, quotient_magnitude), IntegerNumber(remainder_sign, remainder_magnitude)
```