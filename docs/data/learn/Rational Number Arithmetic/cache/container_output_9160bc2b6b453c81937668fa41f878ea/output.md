`{bm-disable-all}`[arithmetic_code/WholeNumber.py](arithmetic_code/WholeNumber.py) (lines 139 to 158):`{bm-enable-all}`

```python
@log_decorator
def __eq__(lhs: WholeNumber, rhs: WholeNumber) -> bool:
    if isinstance(rhs, int):
        rhs = WholeNumber.from_int(rhs)
    elif isinstance(rhs, str):
        rhs = WholeNumber.from_str(rhs)

    if not isinstance(rhs, WholeNumber):
        raise Exception()

    log(f'Equality testing {lhs} and {rhs}...')
    log_indent()

    ret = lhs.digits == rhs.digits

    log_unindent()
    log(f'{ret}')

    return ret
```