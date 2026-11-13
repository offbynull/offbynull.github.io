`{bm-disable-all}`[arithmetic_code/WholeNumber.py](arithmetic_code/WholeNumber.py) (lines 511 to 633):`{bm-enable-all}`

```python
@staticmethod
@log_decorator
def choose_start_test_num_for_divte(input1: WholeNumber, expected_product: WholeNumber) -> WholeNumber:
    log(f'Choosing a starting test number to find {input1} \\* ? = {expected_product}...')
    log_indent()

    log(f'{input1} has {len(input1.digits)} digits')
    log(f'{expected_product}\'s has {len(expected_product.digits)} digits')
    num_of_zeros = len(expected_product.digits) - len(input1.digits)
    start_test_num = WholeNumber.from_str('1' + '0' * num_of_zeros)

    log(f'Starting test number: {start_test_num}')

    log_unindent()
    log(f'{start_test_num}')
    return start_test_num

@staticmethod
@log_decorator
def choose_start_modifier_for_divte(start_test_num: WholeNumber) -> WholeNumber:
    log(f'Choosing a starting modifier for {start_test_num}...')
    log_indent()

    log(f'{start_test_num} has {len(start_test_num.digits)} digits')
    num_of_zeros = len(start_test_num.digits) - 1
    start_modifier_num = WholeNumber.from_str('1' + '0' * num_of_zeros)

    log(f'Starting modifier: {start_modifier_num}')

    log_unindent()
    log(f'{start_modifier_num}')
    return start_modifier_num

@staticmethod
@log_decorator
def trial_and_error_div(dividend: WholeNumber, divisor: WholeNumber) -> (WholeNumber, WholeNumber):
    if divisor == WholeNumber.from_str('0'):
        raise Exception('Cannot divide by 0')

    log(f'Dividing {dividend} and {divisor}...')
    log_indent()

    log(f'Calculating starting test number...')
    test = WholeNumber.choose_start_test_num_for_divte(divisor, dividend)
    log(f'{test}')

    log(f'Calculating starting modifier for test number...')
    modifier = WholeNumber.choose_start_modifier_for_divte(test)
    log(f'{modifier}')

    class StepType(Enum):
        INCREMENTING = 0
        DECREMENTING = 1
        EQUAL = 2

    last_steptype = None
    while True:
        log(f'Testing {test}: {test} * {divisor}...')
        test_res = test * divisor
        log(f'{test_res}')

        log(f'Is {test_res} ==, >, or < to {dividend}? ...')
        log_indent()
        try:
            if test_res == dividend:
                last_steptype = StepType.EQUAL
                log(f'{test_res} == {dividend} -- Found')
                break
            elif test_res > dividend:
                last_steptype = StepType.DECREMENTING
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
                last_steptype = StepType.INCREMENTING
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

        if modifier == WholeNumber.from_str('1'):
            break

        log(f'Reducing modifier for next set of tests...')
        modifier = WholeNumber.from_str(str(modifier)[0:-1])
        log(f'{modifier}')

    # if the last set of tests were incrementing, the test number will be 1 more than where it needs to be moved
    # because the loop increments until it exceeds PAST the dividend
    if StepType.INCREMENTING == last_steptype:
        log(f'Decrementing test number (only happens if last set of tests were incrementing)...')
        if test * divisor > dividend:
            test -= WholeNumber.from_str('1')
        log(f'{test}')

    log (f'Determining remainder...')
    remainder = dividend - (test * divisor)
    log(f'{remainder}')

    log_unindent()
    log(f'Quotient: {test}, Remainder: {remainder}')

    return test, remainder
```