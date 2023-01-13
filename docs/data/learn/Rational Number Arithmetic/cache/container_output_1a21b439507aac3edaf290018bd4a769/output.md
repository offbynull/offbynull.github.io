`{bm-disable-all}`[arithmetic_code/WholeNumber.py](arithmetic_code/WholeNumber.py) (lines 718 to 850):`{bm-enable-all}`

```python
@log_decorator
def to_words(self: WholeNumber) -> str:
    suffixes = [None, 'thousand', 'million', 'billion', 'trillion', 'quadrillion', 'quintillion']

    log(f'Converting {self}...')
    log_indent()

    output = ''

    digits_copy = self.digits[:]
    while not digits_copy == []:
        d1 = digits_copy.pop(0) if digits_copy != [] else None
        d2 = digits_copy.pop(0) if digits_copy != [] else None
        d3 = digits_copy.pop(0) if digits_copy != [] else None

        log(f'Converting group {d3} {d2} {d1}...')
        log_indent()

        txt = ''
        if d3 is not None and d3 != Digit(0):
            if d3.value == Digit(1):
                txt += 'one hundred'
            elif d3.value == Digit(2):
                txt += 'two hundred'
            elif d3.value == Digit(3):
                txt += 'three hundred'
            elif d3.value == Digit(4):
                txt += 'four hundred'
            elif d3.value == Digit(5):
                txt += 'five hundred'
            elif d3.value == Digit(6):
                txt += 'six hundred'
            elif d3.value == Digit(7):
                txt += 'seven hundred'
            elif d3.value == Digit(8):
                txt += 'eight hundred'
            elif d3.value == Digit(9):
                txt += 'nine hundred'
            else:
                raise Exception()

        ignore_first_digit = False
        if d2 is not None and d3 != Digit(0):
            txt += ' '
            if d2.value == Digit(1):
                ignore_first_digit = True
                if d1 == Digit(0):
                    txt += 'ten'
                elif d1 == Digit(1):
                    txt += 'eleven'
                elif d1 == Digit(2):
                    txt += 'twelve'
                elif d1 == Digit(3):
                    txt += 'thirteen'
                elif d1 == Digit(4):
                    txt += 'fourteen'
                elif d1 == Digit(5):
                    txt += 'fifteen'
                elif d1 == Digit(6):
                    txt += 'sixteen'
                elif d1 == Digit(7):
                    txt += 'seventeen'
                elif d1 == Digit(8):
                    txt += 'eighteen'
                elif d1 == Digit(9):
                    txt += 'nineteen'
                else:
                    raise Exception()
            elif d2.value == Digit(2):
                txt += 'twenty'
            elif d2.value == Digit(3):
                txt += 'thirty'
            elif d2.value == Digit(4):
                txt += 'forty'
            elif d2.value == Digit(5):
                txt += 'fifty'
            elif d2.value == Digit(6):
                txt += 'sixty'
            elif d2.value == Digit(7):
                txt += 'seventy'
            elif d2.value == Digit(8):
                txt += 'eighty'
            elif d2.value == Digit(9):
                txt += 'ninety'
            else:
                raise Exception()

        if not ignore_first_digit and d1 is not None and d1 != Digit(0):
            txt += ' '
            if d1.value == Digit(1):
                txt += 'one'
            elif d1.value == Digit(2):
                txt += 'two'
            elif d1.value == Digit(3):
                txt += 'three'
            elif d1.value == Digit(4):
                txt += 'four'
            elif d1.value == Digit(5):
                txt += 'five'
            elif d1.value == Digit(6):
                txt += 'six'
            elif d1.value == Digit(7):
                txt += 'seven'
            elif d1.value == Digit(8):
                txt += 'eight'
            elif d1.value == Digit(9):
                txt += 'nine'
            else:
                raise Exception()

        if suffixes == []:
            raise Exception('Number too large')

        log(f'Words: {txt}')

        suffix = suffixes.pop(0)
        if suffix is not None:
            txt += ' ' + suffix

        log(f'Suffix: {suffix}')
        log_unindent()

        output = txt + ' ' + output

    output = output.lstrip()
    if output == '':
        output = 'zero'

    log_unindent()
    log(f'{output}')

    return output.strip()
```