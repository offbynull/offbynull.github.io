`{bm-disable-all}`[arithmetic_code/FractionNumber.py](arithmetic_code/FractionNumber.py) (lines 285 to 300):`{bm-enable-all}`

```python
@log_decorator
def to_words(self: FractionNumber) -> str:
    log(f'Converting {self}...')

    output = ''
    if self.sign == Sign.NEGATIVE:
        output += 'negative '
    output += self.numerator.to_words()
    output += ' over '
    output += self.denominator.to_words()

    log_unindent()
    log(f'{output}')

    return output.lstrip()
```