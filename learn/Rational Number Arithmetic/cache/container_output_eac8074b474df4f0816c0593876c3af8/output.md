`{bm-disable-all}`[arithmetic_code/IntegerNumber.py](arithmetic_code/IntegerNumber.py) (lines 195 to 208):`{bm-enable-all}`

```python
@log_decorator
def to_words(self: IntegerNumber) -> str:
    log(f'Converting {self}...')

    output = ''
    if self.sign == Sign.NEGATIVE:
        output += 'negative '
    output += self.magnitude.to_words()

    log_unindent()
    log(f'{output}')

    return output.lstrip()
```