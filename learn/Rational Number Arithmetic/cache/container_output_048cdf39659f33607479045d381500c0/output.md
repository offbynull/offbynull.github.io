`{bm-disable-all}`[arithmetic_code/DecimalNumber.py](arithmetic_code/DecimalNumber.py) (lines 765 to 886):`{bm-enable-all}`

```python
@staticmethod
@log_decorator
def choose_start_test_num_for_divte(input1: DecimalNumber, expected_product: DecimalNumber) -> DecimalNumber:
    log(f'Choosing a starting number to find {input1} \\* ? = {expected_product}...')
    log_indent()

    log(f'Checking which case should apply...')
    if input1 < DecimalNumber.from_str('1.0') and expected_product >= DecimalNumber.from_str('1.0'):
        log(f'{input1} has {len(input1.fractional.digits)} fractional digits')
        log(f'{expected_product}\'s has {len(expected_product.whole.digits)} whole digits')
        num_of_zeros = len(expected_product.whole.digits) + len(input1.fractional.digits) - 1
        start_test_num = DecimalNumber.from_str('1' + '0' * num_of_zeros)
    else:
        log(f'{input1} has {len(input1.whole.digits)} whole digits')
        log(f'{expected_product}\'s has {len(expected_product.whole.digits)} whole digits')
        num_of_zeros = len(expected_product.whole.digits) - len(input1.whole.digits)
        start_test_num = DecimalNumber.from_str('1' + '0' * num_of_zeros)

    log(f'Starting number: {start_test_num}')

    log_unindent()
    log(f'{start_test_num}')
    return start_test_num

@staticmethod
@log_decorator
def choose_start_modifier_for_divte(start_test_num: DecimalNumber) -> DecimalNumber:
    log(f'Choosing a starting modifier for {start_test_num}...')
    log_indent()

    log(f'{start_test_num} has {len(start_test_num.whole.digits)} digits')
    num_of_zeros = len(start_test_num.whole.digits) - 1
    start_modifier_num = DecimalNumber.from_str('1' + '0' * num_of_zeros)

    log(f'Starting modifier: {start_modifier_num}')

    log_unindent()
    log(f'{start_modifier_num}')
    return start_modifier_num

@staticmethod
@log_decorator
def trial_and_error_div(dividend: DecimalNumber, divisor: DecimalNumber) -> DecimalNumber:
    log(f'Dividing {dividend} and {divisor}...')
    log_indent()

    log(f'Ensuring {dividend} / {divisor} results in a terminating decimal...')
    if not DecimalNumber.will_division_terminate(dividend, divisor):
        raise Exception('Resulting decimal will be non-terminating')

    log(f'Treating {dividend} and {divisor} as non-negative to perform the algorithm...')
    orig_dividend_sign = dividend.sign
    orig_divisor_sign = divisor.sign
    if dividend.sign == Sign.NEGATIVE:
        dividend *= DecimalNumber.from_str('-1.0')
    if divisor.sign == Sign.NEGATIVE:
        divisor *= DecimalNumber.from_str('-1.0')
    log(f'Non-negative: {dividend} and {divisor}...')

    log(f'Calculating starting test number...')
    test = DecimalNumber.choose_start_test_num_for_divte(divisor, dividend)
    log(f'{test}')

    log(f'Calculating starting modifier for test number...')
    modifier = DecimalNumber.choose_start_modifier_for_divte(test)
    log(f'{modifier}')

    while True:
        log(f'Testing {test}: {test} * {divisor}...')
        test_res = test * divisor
        log(f'{test_res}')

        log(f'Is {test_res} ==, >, or < to {dividend}? ...')
        log_indent()
        try:
            if test_res == dividend:
                log(f'{test_res} == {dividend} -- Found')
                break
            elif test_res > dividend:
                log(f'{test_res} > {dividend} -- Decrementing {test} by {modifier} until not >...')
                log_indent()
                while True:
                    log(f'Decrementing {test} by {modifier}...')
                    test -= modifier
                    log(f'{test} * {divisor}...')
                    modify_res = test * divisor
                    log(f'{modify_res}')
                    if not modify_res > dividend:
                        break
                log_unindent()
                log(f'Done: {test}')
            elif test_res < dividend:
                log(f'{test_res} < {dividend} -- Incrementing {test} by {modifier} until not <...')
                log_indent()
                while True:
                    log(f'Incrementing {test} by {modifier}...')
                    test += modifier
                    log(f'{test} * {divisor}...')
                    modify_res = test * divisor
                    log(f'{modify_res}')
                    if not modify_res < dividend:
                        break
                log_unindent()
                log(f'Done: {test}')
        finally:
            log_unindent()

        log(f'Calculating position for next test...')
        modifier *= DecimalNumber.from_str('0.1')
        log(f'{modifier}')

    log_unindent()
    log(f'{test}')

    log(f'Modifying sign of {test} based on original sign of dividend ({orig_dividend_sign}) and divisor ({orig_divisor_sign})...')
    if orig_dividend_sign == Sign.NEGATIVE and orig_divisor_sign != Sign.NEGATIVE \
            or orig_dividend_sign != Sign.NEGATIVE and orig_divisor_sign == Sign.NEGATIVE:
        test *= DecimalNumber.from_str('-1.0')
    log(f'{test}')

    return test
```