`{bm-disable-all}`[arithmetic_code/WholeNumber.py](arithmetic_code/WholeNumber.py) (lines 287 to 374):`{bm-enable-all}`

```python
@log_decorator
def __sub__(lhs: WholeNumber, rhs: WholeNumber) -> WholeNumber:
    log(f'Subtracting {lhs} and {rhs}...')
    log_indent()

    sub_cache = [
        [0,    None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
        [1,    0,    None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
        [2,    1,    0,    None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
        [3,    2,    1,    0,    None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
        [4,    3,    2,    1,    0,    None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
        [5,    4,    3,    2,    1,    0,    None, None, None, None, None, None, None, None, None, None, None, None, None, None],
        [6,    5,    4,    3,    2,    1,    0,    None, None, None, None, None, None, None, None, None, None, None, None, None],
        [7,    6,    5,    4,    3,    2,    1,    0,    None, None, None, None, None, None, None, None, None, None, None, None],
        [8,    7,    6,    5,    4,    3,    2,    1,    0,    None, None, None, None, None, None, None, None, None, None, None],
        [9,    8,    7,    6,    5,    4,    3,    2,    1,    0,    None, None, None, None, None, None, None, None, None, None],
        [10,   9,    8,    7,    6,    5,    4,    3,    2,    1,    0,    None, None, None, None, None, None, None, None, None],
        [11,   10,   9,    8,    7,    6,    5,    4,    3,    2,    1,    0,    None, None, None, None, None, None, None, None],
        [12,   11,   10,   9,    8,    7,    6,    5,    4,    3,    2,    1,    0,    None, None, None, None, None, None, None],
        [13,   12,   11,   10,   9,    8,    7,    6,    5,    4,    3,    2,    1,    0,    None, None, None, None, None, None],
        [14,   13,   12,   11,   10,   9,    8,    7,    6,    5,    4,    3,    2,    1,    0,    None, None, None, None, None],
        [15,   14,   13,   12,   11,   10,   9,    8,    7,    6,    5,    4,    3,    2,    1,    0,    None, None, None, None],
        [16,   15,   14,   13,   12,   11,   10,   9,    8,    7,    6,    5,    4,    3,    2,    1,    0,    None, None, None],
        [17,   16,   15,   14,   13,   12,   11,   10,   9,    8,    7,    6,    5,    4,    3,    2,    1,    0,    None, None],
        [18,   17,   16,   15,   14,   13,   12,   11,   10,   9,    8,    7,    6,    5,    4,    3,    2,    1,    0,    None],
        [19,   18,   17,   16,   15,   14,   13,   12,   11,   10,   9,    8,    7,    6,    5,    4,    3,    2,    1,    0   ]
    ]

    # copy self because it may get modified during borrowing phase
    self_copy = lhs.copy()

    count = max(len(self_copy.digits), len(rhs.digits))

    result = WholeNumber.from_int(0)
    for pos in range(0, count):  # from smallest to largest component
        log(f'Targeting {self_copy._highlight(pos)} and {rhs._highlight(pos)}')
        log_indent()

        digit1 = self_copy[pos]
        digit2 = rhs[pos]
        result_digit = sub_cache[digit1.value][digit2.value]
        if result_digit is not None:
            log(f'Using cache for subtraction: {digit1} - {digit2} = {result_digit}')
        else:
            log('Not possible -- attempting to borrow')
            self_copy._borrow_from_next(sub_cache, pos)

            digit1 = self_copy[pos]
            digit2 = rhs[pos]
            result_digit = sub_cache[digit1.value][digit2.value]
            log(f'Using cache for subtraction: {digit1} - {digit2} = {result_digit}')

        result[pos] = result_digit
        log(f'Result: {result._highlight(pos)}')
        log_unindent()

    log_unindent()
    log(f'Difference: {result}')

    return result

@log_decorator
def _borrow_from_next(self: WholeNumber, sub_cache: List[List[int]], pos: int) -> None:
    if pos >= len(self):
        raise Exception('Not enough available to borrow')

    curr_digit = self[pos]
    next_digit = self[pos + 1]

    log(f'Borrowing from next largest {self._highlight(pos + 1)}')

    if next_digit == 0:
        log(f'Not possible -- attempting to borrow again')
        self._borrow_from_next(sub_cache, pos + 1)  # recursively borrow
        next_digit = self[pos + 1]  # updated because of borrow call above

    next_digit = sub_cache[next_digit.value][1]                             # sub 1 from next largest position
    curr_digit = (WholeNumber.from_int(10) + WholeNumber.from_digit(curr_digit))._as_digit()    # add 10 to current position

    # curr_digit is no longer an actual digit -- it's beyond the value of 9 (a digit is 0..9). We're using a
    # hack to get a out-of-bounds value as a digit because we need to subtract from it later on -- this is
    # trying to faithfully replicate the 'borrowing' logic in vertical subtraction

    self[pos + 1] = next_digit
    self[pos] = curr_digit

    log(f'Completed borrowing {self._highlight(pos, pos + 1)}')
```