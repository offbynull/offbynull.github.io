`{bm-disable-all}`[arithmetic_code/DecimalNumber.py](arithmetic_code/DecimalNumber.py) (lines 673 to 711):`{bm-enable-all}`

```python
@log_decorator
def __mul__(lhs: DecimalNumber, rhs: DecimalNumber) -> DecimalNumber:
    log(f'Multiplying {lhs} and {rhs}...')
    log_indent()

    adjust_len_self = len(lhs.fractional.digits)
    adjust_len_other = len(rhs.fractional.digits)

    log(f'Generating mock integer number for {lhs}...')
    lhs_extra_0s = adjust_len_self - len(lhs.fractional.digits)
    lhs_combined_digits = lhs.fractional.digits + lhs.whole.digits
    lhs_combined_digits[0:0] = [Digit(0)] * lhs_extra_0s
    mock_self = IntegerNumber(lhs.sign, WholeNumber(lhs_combined_digits))
    log(f'{mock_self}')

    log(f'Generating mock integer number for {rhs}...')
    rhs_extra_0s = adjust_len_other - len(rhs.fractional.digits)
    rhs_combined_digits = rhs.fractional.digits + rhs.whole.digits
    rhs_combined_digits[0:0] = [Digit(0)] * rhs_extra_0s
    mock_other = IntegerNumber(rhs.sign, WholeNumber(rhs_combined_digits))
    log(f'{mock_other}')

    log(f'Performing {mock_self} * {mock_other}...')
    mock_ret = mock_self * mock_other
    log(f'{mock_ret}')

    log(f'Unmocking {mock_ret} back to decimal...')
    unadjust_len = adjust_len_self + adjust_len_other
    ret_sign = mock_ret.sign
    ret_fractional_digits = [mock_ret.magnitude[i] for i in range(0, unadjust_len)]
    ret_whole_digits = [mock_ret.magnitude[i] for i in range(unadjust_len, len(mock_ret.magnitude.digits))]
    ret = DecimalNumber(ret_sign, WholeNumber(ret_whole_digits), FractionalNumber(ret_fractional_digits))
    log(f'{ret}')

    log_unindent()
    log(f'{ret}')

    return ret
```