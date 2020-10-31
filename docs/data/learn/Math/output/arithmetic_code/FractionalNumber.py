from __future__ import annotations

from typing import List, Union

from Digit import Digit
from Output import log_decorator, log, log_indent, log_unindent


# Don't confuse this with FractionNumber...
# * FractionNumber represents a fraction
# * FractionalNumber (this class) represents the part of a decimal number that's past the decimal point
class FractionalNumber:

    @staticmethod
    def from_str(digits: str) -> FractionalNumber:
        digits = list(map(lambda i: Digit(int(i)), digits))
        digits.reverse()
        return FractionalNumber(digits)

    @staticmethod
    def from_digit(digit: Digit) -> FractionalNumber:
        return FractionalNumber.from_digit_list([digit])

    @staticmethod
    def from_digit_list(digits: List[Digit]) -> FractionalNumber:
        return FractionalNumber(digits)

    @staticmethod
    def from_int_list(digits: List[int]) -> FractionalNumber:
        digits = list(map(lambda i: Digit(i), digits))
        return FractionalNumber(digits)

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

    def copy(self: FractionalNumber) -> FractionalNumber:
        return FractionalNumber(self.digits)

    def __getitem__(self, key) -> Digit:
        if key >= len(self.digits):
            return Digit(0)
        return self.digits[len(self.digits) - key - 1]

    def __setitem__(self: FractionalNumber, key: int, value: Union[Digit, int]) -> None:
        if key >= len(self.digits):
            excess = key - len(self.digits) + 1
            self.digits[0:0] = [Digit(0)] * excess  # insert at 0
        if isinstance(value, int):
            self.digits[len(self.digits) - key - 1] = Digit(value)
        elif isinstance(value, Digit):
            self.digits[len(self.digits) - key - 1] = value
        else:
            raise Exception()

        self._prune_unnecessary_0s()

    def __len__(self: FractionalNumber) -> int:
        return len(self.digits)

    def __str__(self: FractionalNumber) -> str:
        output = ''
        for digit in reversed(self.digits):
            output += str(digit.value)
        return output

    def __repr__(self: FractionalNumber):
        return self.__str__()

    def __hash__(self):
        return hash(tuple(self.digits))

    def _prune_unnecessary_0s(self: FractionalNumber) -> None:
        trim_count = 0
        for digit in self.digits:
            if digit == 0:
                trim_count += 1
            else:
                break

        self.digits = self.digits[trim_count:]

        # if empty, keep a single digit there
        if len(self.digits) == 0:
            self.digits = [Digit(0)]

    #MARKDOWN_EQ
    @log_decorator
    def __eq__(lhs: FractionalNumber, rhs: FractionalNumber) -> bool:
        if not isinstance(rhs, FractionalNumber):
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
    def __lt__(lhs: FractionalNumber, rhs: FractionalNumber) -> bool:
        if not isinstance(rhs, FractionalNumber):
            raise Exception()

        log(f'Less than testing {lhs} and {rhs}...')
        log_indent()

        count = max(len(lhs.digits), len(rhs.digits))
        for pos in range(0, count):  # from smallest to largest component
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

    def __le__(lhs: FractionalNumber, rhs: FractionalNumber) -> bool:
        return lhs < rhs or lhs == rhs

    #MARKDOWN_GT
    @log_decorator
    def __gt__(lhs: FractionalNumber, rhs: FractionalNumber) -> bool:
        if not isinstance(rhs, FractionalNumber):
            raise Exception()

        log(f'Greater than testing {lhs} and {rhs}...')
        log_indent()

        count = max(len(lhs.digits), len(rhs.digits))
        for pos in range(0, count):  # from smallest to largest component
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

    def __ge__(self: FractionalNumber, other: FractionalNumber) -> bool:
        return self > other or self == other


if __name__ == '__main__':
    print(f'{FractionalNumber.from_str("401") < FractionalNumber.from_str("45")}')
    print(f'{FractionalNumber.from_str("45") < FractionalNumber.from_str("401")}')

    print(f'{FractionalNumber.from_str("401") > FractionalNumber.from_str("45")}')
    print(f'{FractionalNumber.from_str("45") > FractionalNumber.from_str("401")}')

    print(f'{FractionalNumber.from_str("400") == FractionalNumber.from_str("4")}')
    print(f'{FractionalNumber.from_str("4") == FractionalNumber.from_str("400")}')
    print(f'{FractionalNumber.from_str("4") == FractionalNumber.from_str("401")}')

    # print(f'{PartialNumber.from_str("4")}')
    # print(f'{PartialNumber.from_str("04")}')
    # print(f'{PartialNumber.from_str("040")}')
    # print(f'{PartialNumber.from_str("140")}')
    # print(f'{PartialNumber.from_str("140")[0]}')
    # print(f'{PartialNumber.from_str("140")[1]}')
    # print(f'{PartialNumber.from_str("140")[2]}')
    #
    # test = PartialNumber.from_str("140")
    # print(f'{test}')
    # test[0] = Digit(9)
    # print(f'{test}')
    # test[1] = Digit(8)
    # print(f'{test}')
    # test[4] = Digit(5)
    # print(f'{test}')