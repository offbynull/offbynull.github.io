from __future__ import annotations

from bisect import bisect_left
from collections import OrderedDict
from typing import Union, Optional, Dict

from Output import *
from Digit import Digit


class WholeNumber:

    @staticmethod
    def from_str(digits: str) -> WholeNumber:
        digits = list(map(lambda i: Digit(int(i)), digits))
        digits.reverse()
        return WholeNumber(digits)

    @staticmethod
    def from_int(value: int) -> WholeNumber:
        if value < 0:
            raise Exception('Negative int not allowed')
        digits = str(value)
        digits = list(map(lambda i: Digit(int(i)), digits))
        digits.reverse()
        return WholeNumber(digits)


    @staticmethod
    def from_digit(digit: Digit) -> WholeNumber:
        return WholeNumber.from_digit_list([digit])

    @staticmethod
    def from_digit_list(digits: List[Digit]) -> WholeNumber:
        return WholeNumber(digits)

    @staticmethod
    def from_int_list(digits: List[int]) -> WholeNumber:
        digits = list(map(lambda i: Digit(i), digits))
        return WholeNumber(digits)

    def __init__(self, digits: List[Digit]):
        if digits is None:
            self.digits = [Digit(0)]
        elif isinstance(digits, Digit):
            self.digits = [digits]
        elif isinstance(digits, list):
            self.digits = list(map(lambda i: Digit(i) if isinstance(i, int) else i, digits))
        elif isinstance(digits, str):
            self.digits = list(map(lambda i: Digit(int(i)), digits))
            self.digits.reverse()
        elif isinstance(digits, int):
            if digits < 0:
                raise Exception('Negative int not allowed')
            digits = str(digits)
            self.digits = list(map(lambda i: Digit(int(i)), digits))
            self.digits.reverse()
        else:
            raise Exception()

        self._prune_unnecessary_0s()

    def __getitem__(self: WholeNumber, key: int) -> Digit:
        if key >= len(self.digits):
            return Digit(0)
        return self.digits[key]

    def __setitem__(self: WholeNumber, key: int, value: Union[Digit, int]) -> None:
        if key >= len(self.digits):
            excess = key - len(self.digits) + 1
            self.digits.extend([Digit(0)] * excess)
        if isinstance(value, int):
            self.digits[key] = Digit(value)
        elif isinstance(value, Digit):
            self.digits[key] = value
        else:
            raise Exception()

        self._prune_unnecessary_0s()

    def __len__(self: WholeNumber) -> int:
        return len(self.digits)

    def __str__(self: WholeNumber) -> str:
        output = ''
        for digit in reversed(self.digits):
            output += str(digit.value)
        return output

    def __repr__(self: WholeNumber) -> str:
        return self.__str__()

    def __hash__(self) -> int:
        return hash(tuple(self.digits))

    def _as_int(self: WholeNumber) -> int:
        return int(str(self))

    def _as_digit(self: WholeNumber) -> Digit:
        return Digit(int(str(self)), allowOob=True)

    def _highlight(self: WholeNumber, *idxes: int) -> None:
        digits_copy = self.digits[:]

        max_idxes = max(idxes)
        if max_idxes >= len(digits_copy):
            excess = max_idxes - len(digits_copy) + 1
            digits_copy.extend([Digit(0)] * excess)

        output_str = ''
        for i in range(0, len(digits_copy)):
            dout = str(digits_copy[i].value)
            output_str = ('[' + dout + ']' if i in idxes else dout) + ' ' + output_str
        return output_str

    def shift_left(self: WholeNumber, count: int) -> None:
        for i in range(0, count):
            self.digits.insert(0, Digit(0))
        self._prune_unnecessary_0s()

    def _prune_unnecessary_0s(self: WholeNumber) -> None:
        trim_count = 0
        for digit in reversed(self.digits):
            if digit == 0:
                trim_count += 1
            else:
                break

        self.digits = self.digits[:len(self.digits) - trim_count]

        # if empty, keep a single digit there
        if len(self.digits) == 0:
            self.digits = [Digit(0)]

    def copy(self: WholeNumber) -> WholeNumber:
        return WholeNumber(self.digits)

    #MARKDOWN_EQ
    @log_decorator
    def __eq__(lhs: WholeNumber, rhs: WholeNumber) -> bool:
        if isinstance(rhs, int):
            rhs = WholeNumber.from_int(rhs)
        elif isinstance(rhs, str):
            rhs = WholeNumber.from_str(rhs)

        if not isinstance(rhs, WholeNumber):
            raise Exception()

        log(f'Equality testing {lhs} and {rhs}...')
        log_indent()

        ret = lhs.digits == rhs.digits

        log_unindent()
        log(f'{ret}')

        return ret
    #MARKDOWN_EQ

    #MARKDOWN_LT
    @log_decorator
    def __lt__(lhs: WholeNumber, rhs: WholeNumber) -> bool:
        if isinstance(rhs, int):
            rhs = WholeNumber.from_int(rhs)
        elif isinstance(rhs, str):
            rhs = WholeNumber.from_str(rhs)

        if not isinstance(rhs, WholeNumber):
            raise Exception()

        log(f'Less than testing {lhs} and {rhs}...')
        log_indent()

        count = max(len(lhs.digits), len(rhs.digits))
        for pos in reversed(range(0, count)):  # from smallest to largest component
            log(f'Test digits {lhs[pos]} and {rhs[pos]}...')
            if lhs[pos] > rhs[pos]:
                log(f'{lhs[pos]} > {rhs[pos]} -- {lhs} is NOT less than {rhs}, it is greater than')
                return False
            elif lhs[pos] < rhs[pos]:
                log(f'{lhs[pos]} < {rhs[pos]} -- {lhs} is less than {rhs}')
                return True
            else:
                log(f'{lhs[pos]} == {rhs[pos]} -- continuing testing')

        log(f'No more digits to test -- {lhs} is NOT less than {rhs}, it is equal')
        return False
    #MARKDOWN_LT

    def __le__(lhs: WholeNumber, rhs: WholeNumber) -> bool:
        return lhs < rhs or lhs == rhs

    #MARKDOWN_GT
    @log_decorator
    def __gt__(lhs: WholeNumber, rhs: WholeNumber) -> bool:
        if isinstance(rhs, int):
            rhs = WholeNumber.from_int(rhs)
        elif isinstance(rhs, str):
            rhs = WholeNumber.from_str(rhs)

        if not isinstance(rhs, WholeNumber):
            raise Exception()

        log(f'Greater than testing {lhs} and {rhs}...')
        log_indent()

        count = max(len(lhs.digits), len(rhs.digits))
        for pos in reversed(range(0, count)):  # from smallest to largest component
            log(f'Test digits {lhs[pos]} and {rhs[pos]}...')
            if lhs[pos] > rhs[pos]:
                log(f'{lhs[pos]} > {rhs[pos]} -- {lhs} is greater than {rhs}')
                return True
            elif lhs[pos] < rhs[pos]:
                log(f'{lhs[pos]} < {rhs[pos]} -- {lhs} is NOT greater than {rhs}, it is less than')
                return False
            else:
                log(f'{lhs[pos]} == {rhs[pos]} -- continuing testing')

        log(f'No more digits to test -- {lhs} is NOT greater than {rhs}, it is equal')
        return False
    #MARKDOWN_GT

    def __ge__(lhs: WholeNumber, rhs: WholeNumber) -> bool:
        return lhs > rhs or lhs == rhs

    #MARKDOWN_ADD
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
    #MARKDOWN_ADD

    #MARKDOWN_SUB
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
    #MARKDOWN_SUB

    #MARKDOWN_MUL
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
    #MARKDOWN_MUL

    #MARKDOWN_DIV
    @log_decorator
    def __truediv__(dividend: WholeNumber, divisor: WholeNumber) -> (WholeNumber, WholeNumber):
        if divisor == WholeNumber.from_int(0):
            raise Exception('Cannot divide by 0')

        log(f'Dividing {dividend} by {divisor}...')
        log_indent()

        count = len(dividend.digits)

        quot = WholeNumber.from_int(0)
        rem = WholeNumber.from_int(0)
        for pos in reversed(range(0, count)):  # from largest to smallest component
            log(f'Targeting dividend: {dividend._highlight(pos)}, Current quotient: {quot} / Current remainder: {rem}')
            log_indent()

            comp = dividend[pos]
            if pos == count - 1:  # if this is the start component (largest component)...
                comp_dividend = WholeNumber.from_digit(comp)
                log(f'Set dividend: component ({comp}): {comp_dividend}')
            else:
                temp_rem = rem.copy()
                temp_rem.shift_left(1)
                comp_dividend = WholeNumber.from_digit(comp) + temp_rem
                log(f'Set dividend: Combining prev remainder ({rem}) with component ({comp}): {comp_dividend}')

            comp_quot, comp_rem = WholeNumber.trial_and_error_div(comp_dividend, divisor)
            log(f'Trial-and-error division: {comp_dividend} / {divisor} = {comp_quot}R{comp_rem}')

            new_quot = quot.copy()
            new_quot.shift_left(1)
            new_quot[0] = comp_quot[0]  # comp_quot will always be a single digit
            log(f'New quotient: Combining existing quotient ({quot}) with ({comp_quot}): {new_quot}')
            log(f'New remainder: {comp_rem}')
            quot = new_quot
            rem = comp_rem

            log_unindent()

        log_unindent()
        log(f'Final Quotient: {quot}, Final Remainder: {rem}')

        return quot, rem
    #MARKDOWN_DIV

    #MARKDOWN_DIVTE
    @staticmethod
    @log_decorator
    def choose_start_test_num_for_divte(input1: WholeNumber, expected_product: WholeNumber) -> WholeNumber:
        log(f'Choosing a starting test number to find {input1} \\* ? = {expected_product}...')
        log_indent()

        log(f'{input1} has {len(input1.digits)} digits')
        log(f'{expected_product}\'s has {len(expected_product.digits)} digits')
        num_of_zeros = len(expected_product.digits) - len(input1.digits)
        start_test_num = WholeNumber.from_str('1' + '0' * num_of_zeros)

        log(f'Starting test number: {start_test_num}')

        log_unindent()
        log(f'{start_test_num}')
        return start_test_num

    @staticmethod
    @log_decorator
    def choose_start_modifier_for_divte(start_test_num: WholeNumber) -> WholeNumber:
        log(f'Choosing a starting modifier for {start_test_num}...')
        log_indent()

        log(f'{start_test_num} has {len(start_test_num.digits)} digits')
        num_of_zeros = len(start_test_num.digits) - 1
        start_modifier_num = WholeNumber.from_str('1' + '0' * num_of_zeros)

        log(f'Starting modifier: {start_modifier_num}')

        log_unindent()
        log(f'{start_modifier_num}')
        return start_modifier_num

    @staticmethod
    @log_decorator
    def trial_and_error_div(dividend: WholeNumber, divisor: WholeNumber) -> (WholeNumber, WholeNumber):
        if divisor == WholeNumber.from_str('0'):
            raise Exception('Cannot divide by 0')

        log(f'Dividing {dividend} and {divisor}...')
        log_indent()

        log(f'Calculating starting test number...')
        test = WholeNumber.choose_start_test_num_for_divte(divisor, dividend)
        log(f'{test}')

        log(f'Calculating starting modifier for test number...')
        modifier = WholeNumber.choose_start_modifier_for_divte(test)
        log(f'{modifier}')

        class StepType(Enum):
            INCREMENTING = 0
            DECREMENTING = 1
            EQUAL = 2

        last_steptype = None
        while True:
            log(f'Testing {test}: {test} * {divisor}...')
            test_res = test * divisor
            log(f'{test_res}')

            log(f'Is {test_res} ==, >, or < to {dividend}? ...')
            log_indent()
            try:
                if test_res == dividend:
                    last_steptype = StepType.EQUAL
                    log(f'{test_res} == {dividend} -- Found')
                    break
                elif test_res > dividend:
                    last_steptype = StepType.DECREMENTING
                    log(f'{test_res} > {dividend} -- Decrementing {test} by {modifier} until not >...')
                    log_indent()
                    while True:
                        log(f'Decrementing {test} by {modifier}...')
                        test -= modifier
                        log(f'{test} * {divisor}...')
                        modify_res = test * divisor
                        log(f'{modify_res}')
                        if not modify_res > dividend:
                            break
                    log_unindent()
                    log(f'Done: {test}')
                elif test_res < dividend:
                    last_steptype = StepType.INCREMENTING
                    log(f'{test_res} < {dividend} -- Incrementing {test} by {modifier} until not <...')
                    log_indent()
                    while True:
                        log(f'Incrementing {test} by {modifier}...')
                        test += modifier
                        log(f'{test} * {divisor}...')
                        modify_res = test * divisor
                        log(f'{modify_res}')
                        if not modify_res < dividend:
                            break
                    log_unindent()
                    log(f'Done: {test}')
            finally:
                log_unindent()

            if modifier == WholeNumber.from_str('1'):
                break

            log(f'Reducing modifier for next set of tests...')
            modifier = WholeNumber.from_str(str(modifier)[0:-1])
            log(f'{modifier}')

        # if the last set of tests were incrementing, the test number will be 1 more than where it needs to be moved
        # because the loop increments until it exceeds PAST the dividend
        if StepType.INCREMENTING == last_steptype:
            log(f'Decrementing test number (only happens if last set of tests were incrementing)...')
            if test * divisor > dividend:
                test -= WholeNumber.from_str('1')
            log(f'{test}')

        log (f'Determining remainder...')
        remainder = dividend - (test * divisor)
        log(f'{remainder}')

        log_unindent()
        log(f'Quotient: {test}, Remainder: {remainder}')

        return test, remainder
    #MARKDOWN_DIVTE

    #MARKDOWN_POWIT
    @log_decorator
    def iterative_pow(base: WholeNumber, exponent: WholeNumber) -> WholeNumber:
        log(f'Computing the power of {base} raised to {exponent} ({base}^{exponent})...')
        log_indent()

        power = WholeNumber.from_str('1')
        while exponent > WholeNumber.from_str('0'):
            log(f'Multiplying {power} by {base}...')
            power = power * base
            exponent -= WholeNumber.from_str('1')  # decrement exponent

        log_unindent()
        log(f'Power: {power}')

        return power
    #MARKDOWN_POWIT

    #MARKDOWN_POW
    @log_decorator
    def __pow__(base: WholeNumber, exponent: WholeNumber, modulo=None):
        log(f'Computing the power of {base} raised to {exponent} ({base}^{exponent})...')
        log_indent()

        cache: OrderedDict[WholeNumber, WholeNumber] = OrderedDict()
        cache[WholeNumber.from_str('0')] = WholeNumber.from_str('1')
        cache[WholeNumber.from_str('1')] = base

        def get_closest_lt_or_eq_cached_exp(e):
            key_list = list(cache.keys())
            pos = bisect_left(key_list, e)
            if pos == 0:
                return key_list[0]
            if pos == len(cache):
                return key_list[-1]
            if key_list[pos] == e:
                return e
            else:
                return key_list[pos - 1]

        mult_str = '1'
        power = WholeNumber.from_str('1')
        current_exponent = WholeNumber.from_str('0')
        remaining_exponent = exponent
        while remaining_exponent > WholeNumber.from_str('0'):
            log(f'Step...')
            log_indent()

            log(f'Remaining Exponent: {remaining_exponent} / Power Cache: {[f"{base}^{k}={v}" for k, v in cache.items()]}')

            cached_exponent = get_closest_lt_or_eq_cached_exp(remaining_exponent)
            cached_power = cache[cached_exponent]

            log(f'Next {cached_exponent} of {remaining_exponent} multiplications can be pulled from cache: {base}^{cached_exponent}={cached_power}')

            power *= cached_power
            current_exponent += cached_exponent
            remaining_exponent -= cached_exponent

            mult_str += f'\*{cached_power}'
            log(f'{base}^{current_exponent}={mult_str}={power}')

            cache[current_exponent] = power
            log(f'{base}^{current_exponent}={power} inserted into cache')

            log_unindent()

        log_unindent()
        log(f'Power: {power}')

        return power
    #MARKDOWN_POW

    @staticmethod
    def range(start: WholeNumber, end: WholeNumber, end_inclusive: bool = False) -> WholeNumber:
        i = start.copy()
        while i < end:
            yield i
            i += WholeNumber.from_int(1)
        if end_inclusive:
            yield i

    #MARKDOWN_TO_WORDS
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
    #MARKDOWN_TO_WORDS


class WholeNumberRange:
    def __init__(self, min: WholeNumber, max: WholeNumber):
        self.min = min
        self.max = max

        if min > max:
            raise Exception()


if __name__ == '__main__':
    # n3 = WholeNumber('1000') - WholeNumber('100')
    # print(n3)
    import inspect

    log_whitelist([(inspect.getfile(WholeNumber), 'trial_and_error_div')])
    # print(f'{WholeNumber.trial_and_error_div(WholeNumber.from_str("2617"), WholeNumber.from_str("52"))}')
    print(f'{WholeNumber.trial_and_error_div(WholeNumber.from_str("11"), WholeNumber.from_str("2"))}')
