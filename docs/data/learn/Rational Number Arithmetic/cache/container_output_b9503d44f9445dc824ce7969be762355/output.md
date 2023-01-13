`{bm-disable-all}`[arithmetic_code/FractionalNumber.py](arithmetic_code/FractionalNumber.py) (lines 150 to 172):`{bm-enable-all}`

```python
@log_decorator
def __gt__(lhs: FractionalNumber, rhs: FractionalNumber) -> bool:
    if not isinstance(rhs, FractionalNumber):
        raise Exception()

    log(f'Greater than testing {lhs} and {rhs}...')
    log_indent()

    count = max(len(lhs.digits), len(rhs.digits))
    for pos in range(0, count):  # from smallest to largest component
        log(f'Test digits {lhs[pos]} and {rhs[pos]}...')
        if lhs[pos] > rhs[pos]:
            log(f'{lhs[pos]} > {rhs[pos]} -- {lhs} is greater than {rhs}')
            return True
        elif lhs[pos] < rhs[pos]:
            log(f'{lhs[pos]} < {rhs[pos]} -- {lhs} is NOT greater than {rhs}, it is less than')
            return False
        else:
            log(f'{lhs[pos]} == {rhs[pos]} -- continuing testing')

    log(f'No more digits to test -- {lhs} is NOT greater than {rhs}, it is equal')
    return False
```