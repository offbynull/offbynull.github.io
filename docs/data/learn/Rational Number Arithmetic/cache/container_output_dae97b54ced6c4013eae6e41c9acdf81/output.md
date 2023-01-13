`{bm-disable-all}`[arithmetic_code/WholeNumber.py](arithmetic_code/WholeNumber.py) (lines 377 to 462):`{bm-enable-all}`

```python
@log_decorator
def __mul__(lhs: WholeNumber, rhs: WholeNumber) -> WholeNumber:
    log(f'Multiplying {lhs} and {rhs}...')
    log_indent()

    count = len(rhs.digits)

    res_list = []
    for pos in range(0, count):  # from smallest to largest component
        log(f'Targeting {lhs} and {rhs._highlight(pos)}')
        log_indent()

        self_copy = lhs.copy()    # create a copy
        self_copy.shift_left(pos)  # shift copy (add 0s) based on the digit we're on
        log(f'Appending 0s to multiplicand based on position of multiplier (pos {pos}): {self_copy} {rhs._highlight(pos)}')

        res = self_copy._single_digit_mul(rhs[pos])  # multiply copy by that digit
        log_unindent()

        res_list.append(res)

    log(f'Summing intermediate results to get final result...')
    log_indent()
    final_res = WholeNumber.from_int(0)
    for res in res_list:
        log(f'Adding {res} to {final_res}')
        final_res += res
    log_unindent()

    log_unindent()
    log(f'Product: {final_res}')

    return final_res

@log_decorator
def _single_digit_mul(self: WholeNumber, digit: Digit) -> WholeNumber:
    cache = [
        [0,  0,  0,  0,  0,  0,  0,  0,  0,  0 ],
        [0,  1,  2,  3,  4,  5,  6,  7,  8,  9 ],
        [0,  2,  4,  6,  8,  10, 12, 14, 16, 18],
        [0,  3,  6,  9,  12, 15, 18, 21, 24, 27],
        [0,  4,  8,  12, 16, 20, 24, 28, 32, 36],
        [0,  5,  10, 15, 20, 25, 30, 35, 40, 45],
        [0,  6,  12, 18, 24, 30, 36, 42, 48, 54],
        [0,  7,  14, 21, 28, 35, 42, 49, 56, 63],
        [0,  8,  16, 24, 32, 40, 48, 56, 64, 72],
        [0,  9,  18, 27, 36, 45, 54, 63, 72, 81]
    ]

    count = len(self.digits)

    carryover_digit = None
    result = WholeNumber.from_int(0)
    for pos in range(0, count):  # from smallest to largest component
        log(f'Targeting {self._highlight(pos)} and {digit}')
        log_indent()

        digit1 = self[pos]

        multed = WholeNumber.from_int(cache[digit1.value][digit.value])
        log(f'Using cache for initial mul: {digit1} * {digit} = {multed}')

        if carryover_digit is not None:
            adjusted_multed = multed + WholeNumber.from_digit(carryover_digit)
            log(f'Adding carryover: {multed} + {carryover_digit} = {adjusted_multed}')
            carryover_digit = None
            multed = adjusted_multed

        if len(multed) == 1:
            result[pos] = multed[0]
        elif len(multed) == 2:
            result[pos] = multed[0]      # keep 1s digit
            carryover_digit = multed[1]  # carryover 10s digit
        else:
            raise Exception('This should never happen')

        log(f'Result: {result._highlight(pos)}, Carryover: {carryover_digit}')
        log_unindent()

    if carryover_digit is not None:
        log(f'Remaining carryover: {self._highlight(count)}  [{carryover_digit}]')
        result[count] = carryover_digit
        log(f'Result: {result._highlight(count)}')

    return result
```