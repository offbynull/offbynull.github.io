`{bm-disable-all}`[arithmetic_code/WholeNumber.py](arithmetic_code/WholeNumber.py) (lines 465 to 508):`{bm-enable-all}`

```python
@log_decorator
def __truediv__(dividend: WholeNumber, divisor: WholeNumber) -> (WholeNumber, WholeNumber):
    if divisor == WholeNumber.from_int(0):
        raise Exception('Cannot divide by 0')

    log(f'Dividing {dividend} by {divisor}...')
    log_indent()

    count = len(dividend.digits)

    quot = WholeNumber.from_int(0)
    rem = WholeNumber.from_int(0)
    for pos in reversed(range(0, count)):  # from largest to smallest component
        log(f'Targeting dividend: {dividend._highlight(pos)}, Current quotient: {quot} / Current remainder: {rem}')
        log_indent()

        comp = dividend[pos]
        if pos == count - 1:  # if this is the start component (largest component)...
            comp_dividend = WholeNumber.from_digit(comp)
            log(f'Set dividend: component ({comp}): {comp_dividend}')
        else:
            temp_rem = rem.copy()
            temp_rem.shift_left(1)
            comp_dividend = WholeNumber.from_digit(comp) + temp_rem
            log(f'Set dividend: Combining prev remainder ({rem}) with component ({comp}): {comp_dividend}')

        comp_quot, comp_rem = WholeNumber.trial_and_error_div(comp_dividend, divisor)
        log(f'Trial-and-error division: {comp_dividend} / {divisor} = {comp_quot}R{comp_rem}')

        new_quot = quot.copy()
        new_quot.shift_left(1)
        new_quot[0] = comp_quot[0]  # comp_quot will always be a single digit
        log(f'New quotient: Combining existing quotient ({quot}) with ({comp_quot}): {new_quot}')
        log(f'New remainder: {comp_rem}')
        quot = new_quot
        rem = comp_rem

        log_unindent()

    log_unindent()
    log(f'Final Quotient: {quot}, Final Remainder: {rem}')

    return quot, rem
```