`{bm-disable-all}`[arithmetic_code/WholeNumber.py](arithmetic_code/WholeNumber.py) (lines 227 to 284):`{bm-enable-all}`

```python
@log_decorator
def __add__(lhs: WholeNumber, rhs: WholeNumber) -> WholeNumber:
    log(f'Adding {lhs} and {rhs}...')
    log_indent()

    cache = [
        [0,  1,  2,  3,  4,  5,  6,  7,  8,  9],
        [1,  2,  3,  4,  5,  6,  7,  8,  9, 10],
        [2,  3,  4,  5,  6,  7,  8,  9, 10, 11],
        [3,  4,  5,  6,  7,  8,  9, 10, 11, 12],
        [4,  5,  6,  7,  8,  9, 10, 11, 12, 13],
        [5,  6,  7,  8,  9, 10, 11, 12, 13, 14],
        [6,  7,  8,  9, 10, 11, 12, 13, 14, 15],
        [7,  8,  9, 10, 11, 12, 13, 14, 15, 16],
        [8,  9, 10, 11, 12, 13, 14, 15, 16, 17],
        [9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
    ]

    count = max(len(lhs.digits), len(rhs.digits))

    carryover_digit = None
    result = WholeNumber.from_int(0)
    for pos in range(0, count):  # from smallest to largest component
        log(f'Targeting {lhs._highlight(pos)} and {rhs._highlight(pos)}')
        log_indent()

        digit1 = lhs[pos]
        digit2 = rhs[pos]

        added = WholeNumber.from_int(cache[digit1.value][digit2.value])
        log(f'Using cache for initial add: {digit1} + {digit2} = {added}')

        if carryover_digit is not None:
            log(f'Using recursion for carryover add: {added} + {carryover_digit} = ...')
            added = added + WholeNumber.from_digit(carryover_digit)  # recurse -- this called __add__()
            carryover_digit = None

        if len(added) == 1:
            result[pos] = added[0]
        elif len(added) == 2:
            result[pos] = added[0]      # keep 1s digit
            carryover_digit = added[1]  # carryover 10s digit
        else:
            raise Exception('This should never happen')

        log(f'Result: {result._highlight(pos)}, Carryover: {carryover_digit}')
        log_unindent()

    if carryover_digit is not None:
        log(f'Remaining carryover: {lhs._highlight(count)}  [{carryover_digit}]')
        result[count] = carryover_digit
        log(f'Result: {result._highlight(count)}')

    log_unindent()
    log(f'Sum: {result}')

    return result
```