`{bm-disable-all}`[arithmetic_code/IntegerNumber.py](arithmetic_code/IntegerNumber.py) (lines 211 to 229):`{bm-enable-all}`

```python
@log_decorator
def __eq__(self: IntegerNumber, other: IntegerNumber) -> bool:
    log(f'Equality testing {self} and {other}...')
    log_indent()

    log(f'Testing sign equality ({self.sign} vs {other.sign})...')
    sign_eq = self.sign == other.sign
    log(f'{sign_eq}')

    log(f'Testing magnitude equality ({self.magnitude} vs {other.magnitude})...')
    mag_eq = self.magnitude == other.magnitude
    log(f'{mag_eq}')

    log_unindent()
    ret = sign_eq and mag_eq
    log(f'{ret}')

    return ret
```