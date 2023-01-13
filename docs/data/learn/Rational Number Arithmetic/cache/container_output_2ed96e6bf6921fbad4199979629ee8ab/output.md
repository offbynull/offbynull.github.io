`{bm-disable-all}`[arithmetic_code/DecimalNumber.py](arithmetic_code/DecimalNumber.py) (lines 250 to 313):`{bm-enable-all}`

```python
@log_decorator
def to_words(self: DecimalNumber) -> str:
    fractional_len_to_suffixes = {
        1: 'tenth',
        2: 'hundredth',
        3: 'thousandth',
        4: 'ten-thousandth',
        5: 'hundred-thousandth',
        6: 'millionth',
        7: 'ten-millionth',
        8: 'hundred-millionth',
        9: 'billionth',
        10: 'ten-billionth',
        11: 'hundred-billionth',
        12: 'trillionth',
        13: 'ten-trillionth',
        14: 'hundred-trillionth',
        15: 'quadrillionth',
        16: 'ten-quadrillionth',
        17: 'hundred-quadillionth',
        18: 'quintillionth',
        19: 'ten-quintillionth',
        20: 'hundred-quintillionth',
    }

    log(f'Converting {self}...')
    log_indent()

    log(f'Converting whole portion to words...')
    whole_words = self.whole.to_words()
    log(f'Whole as words: {whole_words}')

    log(f'Converting fractional portion to words...')
    fractional_words = WholeNumber.from_str(str(self.fractional)).to_words()
    log(f'fractional as words: {fractional_words}')

    output = ''
    if self.whole == WholeNumber.from_str('0') and self.fractional == FractionalNumber.from_str('0'):
        output += 'zero'
    else:
        if self.sign == Sign.NEGATIVE:
            output += 'negative '

        if self.whole != WholeNumber.from_str('0'):
            output += whole_words

        if self.whole != WholeNumber.from_str('0') and self.fractional != FractionalNumber.from_str('0'):
            output += ' and '

        if self.fractional != FractionalNumber.from_str('0'):
            output += fractional_words
            suffix = fractional_len_to_suffixes[len(self.fractional.digits)]
            if suffix is None:
                raise Exception('Fractional too large')
            log(f'Fractional suffix: {suffix}')
            if self.fractional != FractionalNumber.from_str('0'):  # pluralize suffix if more than 1
                suffix += 's'
            output += ' ' + suffix

    log_unindent()
    log(f'{output}')

    return output.strip()
```