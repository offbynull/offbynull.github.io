`{bm-disable-all}`[arithmetic_code/DecimalNumber.py](arithmetic_code/DecimalNumber.py) (lines 316 to 421):`{bm-enable-all}`

```python
@log_decorator
def round(self: DecimalNumber, position: str) -> DecimalNumber:
    log(f'Rounding {self} at {position} position...')
    log_indent()

    position = position.strip()
    if position.endswith('s'):
        position = position[:-1]
    position_word_to_index = {
        'hundred-quintillion': 20,
        'ten-quintillion': 19,
        'quintillion': 18,
        'hundred-quadillion': 17,
        'ten-quadrillion': 16,
        'quadrillion': 15,
        'hundred-trillion': 14,
        'ten-trillion': 13,
        'trillion': 12,
        'hundred-billion': 11,
        'ten-billion': 10,
        'billion': 9,
        'hundred-million': 8,
        'ten-million': 7,
        'million': 6,
        'hundred-thousand': 5,
        'ten-thousand': 4,
        'thousand': 3,
        'hundred': 2,
        'ten': 1,
        'one': 0,
        'tenth': -1,
        'hundredth': -2,
        'thousandth': -3,
        'ten-thousandth': -4,
        'hundred-thousandth': -5,
        'millionth': -6,
        'ten-millionth': -7,
        'hundred-millionth': -8,
        'billionth': -9,
        'ten-billionth': -10,
        'hundred-billionth': -11,
        'trillionth': -12,
        'ten-trillionth': -13,
        'hundred-trillionth': -14,
        'quadrillionth': -15,
        'ten-quadrillionth': -16,
        'hundred-quadillionth': -17,
        'quintillionth': -18,
        'ten-quintillionth': -19,
        'hundred-quintillionth': -20,
    }
    position_idx = position_word_to_index[position]
    if position_idx is None:
        raise Exception('Position unknown')

    next_position_idx = position_idx - 1

    log(f'Determining adder based on following position...')
    log_indent()
    log(f'Checking if digit at following position is >= 5...')
    following_digit = WholeNumber.from_digit(self[next_position_idx])
    if following_digit >= WholeNumber.from_str("5"):
        log(f'True ({following_digit} >= 5), deriving adder based on position...')
        if position_idx >= 0:
            adder = DecimalNumber(
                self.sign,
                WholeNumber.from_str('1' + '0' * position_idx),
                FractionalNumber.from_str('0')
            )
        else:
            adder = DecimalNumber(
                self.sign,
                WholeNumber.from_str('0'),
                FractionalNumber.from_str('0' * -(position_idx + 1) + '1')
            )
    else:
        log(f'False ({following_digit} < 5), setting adder to 0...')
        adder = DecimalNumber.from_str('0')
    log_unindent()
    log(f'{adder}')

    log(f'Adding {adder} to {self}...')
    ret = self.copy() + adder
    log(f'{ret}')

    log(f'Truncating all following positions...')
    log_indent()
    if position_idx >= 0:
        for i in range(0, position_idx):
            ret[i] = Digit(0)
            log(f'{ret}')
        for i in range(0, len(self.fractional.digits)):
            ret[-i - 1] = Digit(0)
            log(f'{ret}')
    else:
        for i in range(-position_idx, len(self.fractional.digits)):
            ret[-i - 1] = Digit(0)
            log(f'{ret}')
    log_unindent()
    log(f'{ret}')

    log_unindent()
    log(f'{ret}')

    return ret
```