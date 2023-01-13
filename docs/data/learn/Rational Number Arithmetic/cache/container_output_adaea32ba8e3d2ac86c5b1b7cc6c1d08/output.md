`{bm-disable-all}`[arithmetic_code/WholeNumber.py](arithmetic_code/WholeNumber.py) (lines 161 to 188):`{bm-enable-all}`

```python
@log_decorator
def __lt__(lhs: WholeNumber, rhs: WholeNumber) -> bool:
    if isinstance(rhs, int):
        rhs = WholeNumber.from_int(rhs)
    elif isinstance(rhs, str):
        rhs = WholeNumber.from_str(rhs)

    if not isinstance(rhs, WholeNumber):
        raise Exception()

    log(f'Less than testing {lhs} and {rhs}...')
    log_indent()

    count = max(len(lhs.digits), len(rhs.digits))
    for pos in reversed(range(0, count)):  # from smallest to largest component
        log(f'Test digits {lhs[pos]} and {rhs[pos]}...')
        if lhs[pos] > rhs[pos]:
            log(f'{lhs[pos]} > {rhs[pos]} -- {lhs} is NOT less than {rhs}, it is greater than')
            return False
        elif lhs[pos] < rhs[pos]:
            log(f'{lhs[pos]} < {rhs[pos]} -- {lhs} is less than {rhs}')
            return True
        else:
            log(f'{lhs[pos]} == {rhs[pos]} -- continuing testing')

    log(f'No more digits to test -- {lhs} is NOT less than {rhs}, it is equal')
    return False
```