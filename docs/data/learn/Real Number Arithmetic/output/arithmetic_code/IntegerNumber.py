from __future__ import annotations

from enum import Enum
from typing import Union

from Sign import Sign
from Output import log_indent, log_unindent, log, log_decorator
from WholeNumber import WholeNumber


class IntegerNumber:
    @staticmethod
    def from_str(val: str) -> IntegerNumber:
        if len(val) == 0:
            raise Exception('Must contain at least 1 char')

        if val.startswith('-'):
            sign = Sign.NEGATIVE
            digits = val[1:]  # remove negative sign
        else:
            sign = Sign.POSITIVE
            digits = val

        magnitude = WholeNumber.from_str(digits)

        if magnitude == WholeNumber.from_int(0):
            sign = None

        return IntegerNumber(sign, magnitude)

    @staticmethod
    def from_whole(val: WholeNumber) -> IntegerNumber:
        return IntegerNumber(None if val == WholeNumber.from_int(0) else Sign.POSITIVE, val)

    @staticmethod
    def from_int(val: int) -> IntegerNumber:
        return IntegerNumber.from_str(str(val))

    def __init__(self, sign: Union[Sign, None], magnitude: WholeNumber):
        self.sign = sign
        self.magnitude = magnitude.copy()

        if magnitude == WholeNumber.from_int(0) and sign is not None:
            raise Exception('Magnitude of 0 cannot have a sign')

    def copy(self: IntegerNumber):
        return IntegerNumber(self.sign, self.magnitude)

    #MARKDOWN_ADD
    @log_decorator
    def __add__(lhs: IntegerNumber, rhs: IntegerNumber) -> IntegerNumber:
        log(f'Adding {lhs} and {rhs}')
        log_indent()

        def determine_sign(magnitude: WholeNumber, default_sign: Sign) -> Sign:
            if magnitude == WholeNumber.from_int(0):
                return None
            else:
                return default_sign

        if lhs.sign is None:  # sign of None is only when magnitude is 0,  0 + a = a
            sign = rhs.sign
            magnitude = rhs.magnitude
        elif rhs.sign is None:  # sign of None is only when magnitude is 0,  a + 0 = a
            sign = lhs.sign
            magnitude = lhs.magnitude
        elif lhs.sign == rhs.sign:
            magnitude = lhs.magnitude + rhs.magnitude
            sign = determine_sign(magnitude, lhs.sign)
        elif lhs.sign != rhs.sign:
            if rhs.magnitude >= lhs.magnitude:
                magnitude = rhs.magnitude - lhs.magnitude
                sign = determine_sign(magnitude, rhs.sign)
            else:
                magnitude = lhs.magnitude - rhs.magnitude
                sign = determine_sign(magnitude, lhs.sign)

        log_unindent()
        log(f'sign: {sign}, magnitude: {magnitude}')

        return IntegerNumber(sign, magnitude)
    #MARKDOWN_ADD

    #MARKDOWN_SUB
    @log_decorator
    def __sub__(lhs: IntegerNumber, rhs: IntegerNumber) -> IntegerNumber:
        log(f'Subtracting {lhs} and {rhs}')
        log_indent()

        def determine_sign(magnitude: WholeNumber, default_sign: Sign) -> Sign:
            if magnitude == WholeNumber.from_int(0):
                return None
            else:
                return default_sign

        def flip_sign(sign: Sign) -> Sign:
            if sign == Sign.POSITIVE:
                return Sign.NEGATIVE
            elif sign == Sign.NEGATIVE:
                return Sign.POSITIVE

        if lhs.sign is None:  # sign of None is only when magnitude is 0,  0 - a = -a
            sign = flip_sign(rhs.sign)
            magnitude = rhs.magnitude
        elif rhs.sign is None:  # sign of None is only when magnitude is 0,  a - 0 = a
            sign = lhs.sign
            magnitude = lhs.magnitude
        elif lhs.sign == rhs.sign:
            if rhs.magnitude >= lhs.magnitude:
                magnitude = rhs.magnitude - lhs.magnitude
                sign = determine_sign(magnitude, flip_sign(lhs.sign))
            else:
                magnitude = lhs.magnitude - rhs.magnitude
                sign = determine_sign(magnitude, lhs.sign)
        elif lhs.sign != rhs.sign:
            magnitude = lhs.magnitude + rhs.magnitude
            sign = determine_sign(magnitude, lhs.sign)

        log_unindent()
        log(f'sign: {sign}, magnitude: {magnitude}')

        return IntegerNumber(sign, magnitude)
    #MARKDOWN_SUB

    #MARKDOWN_MUL
    @log_decorator
    def __mul__(lhs: IntegerNumber, rhs: IntegerNumber) -> IntegerNumber:
        log(f'Multiplying {lhs} and {rhs}')
        log_indent()

        def determine_sign(magnitude: WholeNumber, default_sign: Sign) -> Sign:
            if magnitude == WholeNumber.from_int(0):
                return None
            else:
                return default_sign

        if lhs.sign is None:  # when sign isn't set, magnitude is always 0 -- 0 * a = 0
            sign = None
            magnitude = WholeNumber.from_int(0)
        elif rhs.sign is None:  # when sign isn't set, magnitude is always 0 -- a * 0 = 0
            sign = None
            magnitude = WholeNumber.from_int(0)
        elif (lhs.sign == Sign.POSITIVE and rhs.sign == Sign.POSITIVE) \
                or (lhs.sign == Sign.NEGATIVE and rhs.sign == Sign.NEGATIVE):
            magnitude = lhs.magnitude * rhs.magnitude
            sign = determine_sign(magnitude, Sign.POSITIVE)
        elif (lhs.sign == Sign.POSITIVE and rhs.sign == Sign.NEGATIVE) \
                or (lhs.sign == Sign.NEGATIVE and rhs.sign == Sign.POSITIVE):
            magnitude = lhs.magnitude * rhs.magnitude
            sign = determine_sign(magnitude, Sign.NEGATIVE)

        log_unindent()
        log(f'sign: {sign}, magnitude: {magnitude}')

        return IntegerNumber(sign, magnitude)
    #MARKDOWN_MUL

    #MARKDOWN_DIV
    @log_decorator
    def __truediv__(lhs: IntegerNumber, rhs: IntegerNumber) -> (IntegerNumber, IntegerNumber):
        log(f'Dividing {lhs} and {rhs}')
        log_indent()

        def determine_sign(magnitude: WholeNumber, default_sign: Sign) -> Sign:
            if magnitude == WholeNumber.from_int(0):
                return None
            else:
                return default_sign

        if lhs.sign is None:  # when sign isn't set, magnitude is always 0 -- 0 / a = 0
            (quotient_magnitude, remainder_magnitude) = lhs.magnitude / rhs.magnitude
            quotient_sign = None
            remainder_sign = None
        elif rhs.sign is None:  # when sign isn't set, magnitude is always 0 -- a / 0 = err
            raise Exception('Cannot divide by 0')
        elif (lhs.sign == Sign.POSITIVE and rhs.sign == Sign.POSITIVE) \
                or (lhs.sign == Sign.NEGATIVE and rhs.sign == Sign.NEGATIVE):
            (quotient_magnitude, remainder_magnitude) = lhs.magnitude / rhs.magnitude
            quotient_sign = determine_sign(quotient_magnitude, Sign.POSITIVE)
            remainder_sign = determine_sign(remainder_magnitude, Sign.POSITIVE)
        elif (lhs.sign == Sign.POSITIVE and rhs.sign == Sign.NEGATIVE) \
                or (lhs.sign == Sign.NEGATIVE and rhs.sign == Sign.POSITIVE):
            (quotient_magnitude, remainder_magnitude) = lhs.magnitude / rhs.magnitude
            quotient_sign = determine_sign(quotient_magnitude, Sign.NEGATIVE)
            remainder_sign = determine_sign(remainder_magnitude, Sign.NEGATIVE)

        log_unindent()
        log(f'QUOTIENT: sign: {quotient_sign}, magnitude: {quotient_magnitude}')
        log(f'REMAINDER: sign: {remainder_sign}, magnitude: {remainder_magnitude}')

        return IntegerNumber(quotient_sign, quotient_magnitude), IntegerNumber(remainder_sign, remainder_magnitude)
    #MARKDOWN_DIV

    #MARKDOWN_TO_WORDS
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
    #MARKDOWN_TO_WORDS

    #MARKDOWN_EQ
    @log_decorator
    def __eq__(self: IntegerNumber, other: IntegerNumber) -> bool:
        log(f'Equality testing {self} and {other}...')
        log_indent()

        log(f'Testing sign equality ({self.sign} vs {other.sign})...')
        sign_eq = self.sign == other.sign
        log(f'{sign_eq}')

        log(f'Testing magnitude equality ({self.magnitude} vs {other.magnitude})...')
        mag_eq = self.magnitude == other.magnitude
        log(f'{mag_eq}')

        log_unindent()
        ret = sign_eq and mag_eq
        log(f'{ret}')

        return ret
    #MARKDOWN_EQ

    #MARKDOWN_LT
    @log_decorator
    def __lt__(self: IntegerNumber, other: IntegerNumber) -> bool:
        log(f'Less than testing {self} and {other}...')
        log_indent()

        self_sign = self.sign
        if self_sign is None:  # assume 0 is a positive -- it simplifies logic below
            self_sign = Sign.POSITIVE

        other_sign = other.sign
        if other_sign is None:  # assume 0 is a positive -- it simplifies logic below
            other_sign = Sign.POSITIVE

        if self_sign == Sign.POSITIVE and other_sign == Sign.POSITIVE:
            log(f'{self.sign} < {other.sign}: Applying whole number less than...')
            ret = self.magnitude < other.magnitude
        elif self_sign == Sign.NEGATIVE and other_sign == Sign.NEGATIVE:
            log(f'{self.sign} < {other.sign}: Turning positive and applying whole number greater than...')
            ret = self.magnitude > other.magnitude
        elif self_sign == Sign.POSITIVE and other_sign == Sign.NEGATIVE:
            log(f'{self.sign} < {other.sign}:: Different signs -- number being tested is positive...')
            ret = False
        elif self_sign == Sign.NEGATIVE and other_sign == Sign.POSITIVE:
            log(f'{self.sign} < {other.sign}: Different signs -- number being tested is negative...')
            ret = True
        log(f'{ret}')

        log_unindent()
        log(f'{ret}')

        return ret
    #MARKDOWN_LT

    def __le__(self: IntegerNumber, other: IntegerNumber) -> bool:
        return self < other or self == other

    #MARKDOWN_GT
    @log_decorator
    def __gt__(self: IntegerNumber, other: IntegerNumber) -> bool:
        log(f'Greater than testing {self} and {other}...')
        log_indent()

        self_sign = self.sign
        if self_sign is None:  # assume 0 is a positive -- it simplifies logic below
            self_sign = Sign.POSITIVE

        other_sign = other.sign
        if other_sign is None:  # assume 0 is a positive -- it simplifies logic below
            other_sign = Sign.POSITIVE

        if self_sign == Sign.POSITIVE and other_sign == Sign.POSITIVE:
            log(f'{self.sign} > {other.sign}: Applying whole number less than...')
            ret = self.magnitude > other.magnitude
        elif self_sign == Sign.NEGATIVE and other_sign == Sign.NEGATIVE:
            log(f'{self.sign} > {other.sign}: Turning positive and applying whole number greater than...')
            ret = self.magnitude < other.magnitude
        elif self_sign == Sign.POSITIVE and other_sign == Sign.NEGATIVE:
            log(f'{self.sign} > {other.sign}:: Different signs -- number being tested is positive...')
            ret = True
        elif self_sign == Sign.NEGATIVE and other_sign == Sign.POSITIVE:
            log(f'{self.sign} > {other.sign}: Different signs -- number being tested is negative...')
            ret = False
        log(f'{ret}')

        log_unindent()
        log(f'{ret}')

        return ret
    #MARKDOWN_GT

    def __ge__(self: IntegerNumber, other: IntegerNumber) -> bool:
        return self > other or self == other

    def __str__(self: IntegerNumber) -> str:
        if self.sign == Sign.POSITIVE:
            ret = '+'
        elif self.sign == Sign.NEGATIVE:
            ret = '-'
        else:
            ret = ''
        ret += str(self.magnitude)
        return ret

    def __repr__(self: IntegerNumber) -> str:
        return self.__str__()

    def __hash__(self: IntegerNumber) -> int:
        return hash(tuple([self.sign, self.magnitude]))


if __name__ == '__main__':
    # mag, rem = IntegerNumber.from_int(-30) / IntegerNumber.from_int(-5)
    # print(f'{mag}R{rem}')

    # print(f'{IntegerNumber.from_int(30) * IntegerNumber.from_int(5)}')

    # print(f'{IntegerNumber.from_int(2) - IntegerNumber.from_int(1)}')
    # print(f'{IntegerNumber.from_int(-2) - IntegerNumber.from_int(-1)}')
    # print(f'{IntegerNumber.from_int(2) - IntegerNumber.from_int(-1)}')
    # print(f'{IntegerNumber.from_int(-2) - IntegerNumber.from_int(1)}')
    # print(f'{IntegerNumber.from_int(0) - IntegerNumber.from_int(2)}')
    # print(f'{IntegerNumber.from_int(2) - IntegerNumber.from_int(0)}')
    # print(f'{IntegerNumber.from_int(0) - IntegerNumber.from_int(0)}')
    # print(f'{IntegerNumber.from_int(2) - IntegerNumber.from_int(2)}')
    # print(f'{IntegerNumber.from_int(-2) - IntegerNumber.from_int(-2)}')

    print(f'{IntegerNumber.from_int(-2249) == IntegerNumber.from_int(-2249)}')
    print(f'{IntegerNumber.from_int(-2249) == IntegerNumber.from_int(2249)}')
    print(f'{IntegerNumber.from_int(-2249) == IntegerNumber.from_int(0)}')
