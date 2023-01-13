`{bm-disable-all}`[arithmetic_code/DecimalNumber.py](arithmetic_code/DecimalNumber.py) (lines 463 to 520):`{bm-enable-all}`

```python
@log_decorator
def __lt__(lhs: DecimalNumber, rhs: DecimalNumber) -> bool:
    class PassedTestException(Exception):
        pass

    class FailedTestException(Exception):
        pass

    log(f'Less than testing {lhs} and {rhs}...')
    log_indent()

    try:
        log(f'Testing sign...')
        sign_lt = (lhs.sign == Sign.NEGATIVE or lhs.sign is None) and rhs.sign == Sign.POSITIVE
        if sign_lt:
            raise PassedTestException()
        sign_eq = lhs.sign == rhs.sign
        if not sign_eq:
            raise FailedTestException()
        log(f'Equal')

        log(f'Testing whole...')
        if lhs.sign != Sign.NEGATIVE:
            whole_lt = lhs.whole < rhs.whole
        else:
            whole_lt = lhs.whole > rhs.whole
        if whole_lt:
            raise PassedTestException()
        whole_eq = lhs.whole == rhs.whole
        if not whole_eq:
            raise FailedTestException()
        log(f'Equal')

        log(f'Testing fractional...')
        if lhs.sign != Sign.NEGATIVE:
            fractional_lt = lhs.fractional < rhs.fractional
        else:
            fractional_lt = lhs.fractional > rhs.fractional
        if fractional_lt:
            raise PassedTestException()
        fractional_eq = lhs.fractional == rhs.fractional
        if not fractional_eq:
            raise FailedTestException()
        log(f'Equal')

        ret = False
    except PassedTestException:
        log(f'Less')
        ret = True
    except FailedTestException:
        log(f'Not less or equal')
        ret = False

    log_unindent()
    log(f'{ret}')

    return ret
```