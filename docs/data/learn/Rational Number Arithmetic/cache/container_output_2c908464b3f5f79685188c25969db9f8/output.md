`{bm-disable-all}`[arithmetic_code/DecimalNumber.py](arithmetic_code/DecimalNumber.py) (lines 715 to 760):`{bm-enable-all}`

```python
@staticmethod
@log_decorator
def will_division_terminate(lhs: DecimalNumber, rhs: DecimalNumber) -> bool:
    log(f'Checking if {lhs} / {rhs} results in a non-terminating decimal...')
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

    log(f'Generating mock fraction for {lhs} / {rhs}...')
    mock_fraction = FractionNumber(mock_self, mock_other)
    log(f'{mock_fraction}')

    log(f'Simplifying mock fraction...')
    mock_fraction = mock_fraction.simplify()
    log(f'{mock_fraction}')

    log(f'Checking if prime factors of denom ({mock_fraction.denominator}) is {{}}, {{2}}, {{5}}, or {{2,5}}...')
    mock_fraction_denom_prime_factors = set(factor_tree(mock_fraction.denominator).get_prime_factors())
    if not ({WholeNumber.from_str('2'), WholeNumber.from_str('5')} == mock_fraction_denom_prime_factors
            or {WholeNumber.from_str('2')} == mock_fraction_denom_prime_factors
            or {WholeNumber.from_str('5')} == mock_fraction_denom_prime_factors
            or 0 == len(mock_fraction_denom_prime_factors)):
        ret = False
        log(f'{ret} -- Won\'t terminate.')
    else:
        ret = True
        log(f'{ret} -- Will terminate.')

    log_unindent()
    log(f'{ret}')
    return ret
```