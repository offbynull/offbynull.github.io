`{bm-disable-all}`[arithmetic_code/DecimalNumber.py](arithmetic_code/DecimalNumber.py) (lines 526 to 583):`{bm-enable-all}`

```python
@log_decorator
def __gt__(lhs: DecimalNumber, rhs: DecimalNumber) -> bool:
    class PassedTestException(Exception):
        pass

    class FailedTestException(Exception):
        pass

    log(f'Greater than testing {lhs} and {rhs}...')
    log_indent()

    try:
        log(f'Testing sign...')
        sign_gt = lhs.sign == Sign.POSITIVE and (rhs.sign == Sign.NEGATIVE or rhs.sign is None)
        if sign_gt:
            raise PassedTestException()
        sign_eq = lhs.sign == rhs.sign
        if not sign_eq:
            raise FailedTestException()
        log(f'Equal')

        log(f'Testing whole...')
        if lhs.sign != Sign.NEGATIVE:
            whole_gt = lhs.whole > rhs.whole
        else:
            whole_gt = lhs.whole < rhs.whole
        if whole_gt:
            raise PassedTestException()
        whole_eq = lhs.whole == rhs.whole
        if not whole_eq:
            raise FailedTestException()
        log(f'Equal')

        log(f'Testing fractional...')
        if lhs.sign != Sign.NEGATIVE:
            fractional_gt = lhs.fractional > rhs.fractional
        else:
            fractional_gt = lhs.fractional < rhs.fractional
        if fractional_gt:
            raise PassedTestException()
        fractional_eq = lhs.fractional == rhs.fractional
        if not fractional_eq:
            raise FailedTestException()
        log(f'Equal')

        ret = False
    except PassedTestException:
        log(f'Greater')
        ret = True
    except FailedTestException:
        log(f'Not greater or equal')
        ret = False

    log_unindent()
    log(f'{ret}')

    return ret
```