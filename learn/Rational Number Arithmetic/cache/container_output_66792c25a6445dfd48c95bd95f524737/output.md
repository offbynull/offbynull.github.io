`{bm-disable-all}`[arithmetic_code/DecimalNumber.py](arithmetic_code/DecimalNumber.py) (lines 424 to 460):`{bm-enable-all}`

```python
@log_decorator
def __eq__(lhs: DecimalNumber, rhs: DecimalNumber) -> bool:
    class FailedTestException(Exception):
        pass

    log(f'Equality testing {lhs} and {rhs}...')
    log_indent()

    try:
        log(f'Testing sign...')
        sign_eq = lhs.sign == rhs.sign
        if not sign_eq:
            raise FailedTestException()
        log(f'Equal')

        log(f'Testing whole...')
        whole_eq = lhs.whole == rhs.whole
        if not whole_eq:
            raise FailedTestException()
        log(f'Equal')

        log(f'Testing fractional...')
        fractional_eq = lhs.fractional == rhs.fractional
        if not fractional_eq:
            raise FailedTestException()
        log(f'Equal')

        ret = True
    except FailedTestException:
        log(f'Not equal')
        ret = False

    log_unindent()
    log(f'{ret}')

    return ret
```