`{bm-disable-all}`[arithmetic_code/FractionalNumber.py](arithmetic_code/FractionalNumber.py) (lines 105 to 119):`{bm-enable-all}`

```python
@log_decorator
def __eq__(lhs: FractionalNumber, rhs: FractionalNumber) -> bool:
    if not isinstance(rhs, FractionalNumber):
        raise Exception()

    log(f'Equality testing {lhs} and {rhs}...')
    log_indent()

    ret = lhs.digits == rhs.digits

    log_unindent()
    log(f'{ret}')

    return ret
```