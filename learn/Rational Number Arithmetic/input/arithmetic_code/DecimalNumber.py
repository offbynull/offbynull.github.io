from __future__ import annotations

import inspect
from typing import Union

from Digit import Digit
from Factor import factor_tree
from FractionNumber import FractionNumber
from IntegerNumber import IntegerNumber
from Output import log, log_indent, log_unindent, log_decorator, log_whitelist
from FractionalNumber import FractionalNumber
from Sign import Sign
from WholeNumber import WholeNumber


class DecimalNumber:

    @staticmethod
    def from_str(val: str) -> DecimalNumber:
        values = val.split('.')
        if len(values) == 1 and len(values[0]) > 0:
            return DecimalNumber.from_integer(
                IntegerNumber.from_str(values[0])
            )
        elif len(values) == 2:
            if values[0][0] == '-':
                sign = Sign.NEGATIVE
                values[0] = values[0][1:]
            elif values[0][0] == '+':
                sign = Sign.POSITIVE
                values[0] = values[0][1:]
            elif values[0] == '0':
                sign = None
            else:
                sign = Sign.POSITIVE

            whole = FractionNumber(
                IntegerNumber.from_whole(WholeNumber.from_str(values[0])),
                IntegerNumber.from_str('1')
            )
            fractional = FractionNumber(
                IntegerNumber.from_whole(WholeNumber.from_str(values[1])),
                IntegerNumber.from_whole(WholeNumber.from_str('1' + ('0' * len(values[1]))))
            )

            final_frac = whole + fractional
            if sign == Sign.NEGATIVE:
                final_frac = final_frac * FractionNumber.from_str("-1/1")

            return DecimalNumber.from_fraction(final_frac)
        else:
            raise Exception(f'Bad format: {val}')

    @staticmethod
    def from_whole(value: WholeNumber) -> DecimalNumber:
        return DecimalNumber.from_fraction(FractionNumber.from_whole(value))

    @staticmethod
    def from_integer(value: IntegerNumber) -> DecimalNumber:
        return DecimalNumber.from_fraction(FractionNumber.from_integer(value))

    @staticmethod
    def from_int(value: int) -> DecimalNumber:
        return DecimalNumber.from_fraction(FractionNumber.from_int(value))

    #MARKDOWN_FROM_FRAC
    @staticmethod
    @log_decorator
    def from_fraction(value: FractionNumber) -> DecimalNumber:
        log(f'Converting {value} to a decimal number...')
        log_indent()

        log(f'Converting {value} to suitable fraction...')
        value = DecimalNumber.to_suitable_fraction(value)
        log(f'{value}')

        num = value.numerator
        denom = value.denominator
        if not str(denom).startswith('1'):
            raise Exception('Denominator must be power of 10')
        elif not set(str(denom)[1:]) == set('0') and not set(str(denom)[1:]) == set():
            raise Exception('Denominator must be power of 10')

        log(f'Resolving fraction {value}...')
        whole, remaining = num / denom
        log(f'{whole} wholes and {remaining} remaining')

        log(f'Converting {remaining} of {denom} to fractional value...')
        num_digits_in_rem = len(remaining.digits)
        num_0s_in_den = len(denom.digits) - 1  # starts with 1 followed by 0s, so - 1 to ignore the starting 1
        num_0s_to_prepend_to_rem = num_0s_in_den - num_digits_in_rem
        fractional_digits = remaining.digits[:]  # copy digits
        fractional_digits = fractional_digits + [Digit(0)] * num_0s_to_prepend_to_rem  # this prepending 0s...
                                                                                   # you might be confused because the
                                                                                   # 0s are being addeed to the end, but
                                                                                   # that's how FractionalNumber expects
                                                                                   # digits -- in reversed order
        fractional = FractionalNumber(fractional_digits)
        log(f'{fractional}')

        sign = value.sign

        log_unindent()

        ret = DecimalNumber(sign, whole, fractional)
        log(f'Decimal number: {ret}')
        return ret
    #MARKDOWN_FROM_FRAC

    #MARKDOWN_TO_SUITABLE_FRAC
    @staticmethod
    @log_decorator
    def to_suitable_fraction(value: FractionNumber) -> FractionNumber:
        log(f'Converting {value} to an equivalent fraction with denominator that is power of 10...')
        log_indent()

        denom = value.denominator

        if str(denom)[0] == '1' and (set(str(denom)[1:]) == set() or set(str(denom)[1:]) == set('0')):
            log(f'Already power of 10')
        else:
            log(f'No')
            log(f'Simplifying fraction {value}...')
            value = value.simplify()
            denom = value.denominator
            log(f'{value}')

            log(f'Calculating unique prime factors of {denom}...')
            denom_prime_factors = factor_tree(denom).get_prime_factors()
            denom_prime_factors_set = set(denom_prime_factors)
            log(f'{denom_prime_factors_set}')
            if not({WholeNumber.from_int(2), WholeNumber.from_int(5)} == denom_prime_factors_set
                   or {WholeNumber.from_int(2)} == denom_prime_factors_set
                   or {WholeNumber.from_int(5)} == denom_prime_factors_set
                   or 0 == len(denom_prime_factors_set)):
                raise Exception('Simplified denominator contains prime factors other than 2 and 5')

            log(f'Calculating value to scale by so {denom} becomes next largest power of 10...')
            num_of_2s = len(list(filter(lambda pf: pf == WholeNumber.from_str('2'), denom_prime_factors)))
            num_of_5s = len(list(filter(lambda pf: pf == WholeNumber.from_str('5'), denom_prime_factors)))
            extra_2s = 0
            extra_5s = 0
            if num_of_2s == 0 and num_of_5s == 0:
                extra_2s = 1
                extra_5s = 1
            elif num_of_2s < num_of_5s:
                extra_2s = num_of_5s - num_of_2s
            elif num_of_2s > num_of_5s:
                extra_5s = num_of_2s - num_of_5s
            log(f'Require {extra_2s} 2s and {extra_5s} 5s')

            log(f'Multiplying {extra_2s} 2s and {extra_5s} 5s to get scale...')
            scale_by = WholeNumber.from_str('1')
            for i in range(extra_2s):
                scale_by *= WholeNumber.from_str('2')
            for i in range(extra_5s):
                scale_by *= WholeNumber.from_str('5')
            log(f'{scale_by}')

            log(f'Multiplying {value}\'s numerator and denominator by {scale_by}...')
            value = value * FractionNumber(
                IntegerNumber.from_whole(scale_by),
                IntegerNumber.from_whole(scale_by)
            )
            log(f'{value}')

        log_unindent()
        log(f'{value}')

        return value
    #MARKDOWN_TO_SUITABLE_FRAC

    def __init__(self, sign: Union[Sign, None], whole: WholeNumber, fractional: FractionalNumber):
        self.sign = sign
        self.whole = whole.copy()
        self.fractional = fractional.copy()

        if whole == WholeNumber.from_str('0') and fractional == FractionalNumber.from_str('0') and sign is not None:
            raise Exception('Magnitude of 0 cannot have a sign')

    def copy(self: DecimalNumber) -> DecimalNumber:
        return DecimalNumber(self.sign, self.whole, self.fractional)

    def __str__(self: DecimalNumber):
        if self.sign == Sign.POSITIVE:
            ret = '+'
        elif self.sign == Sign.NEGATIVE:
            ret = '-'
        else:
            ret = ''

        ret += str(self.whole) + '.' + str(self.fractional)

        return ret

    def __repr__(self: DecimalNumber) -> str:
        return self.__str__()

    def __hash__(self: DecimalNumber) -> int:
        return hash(tuple([self.sign, self.whole, self.fractional]))

    def __getitem__(self: DecimalNumber, key: int) -> Digit:
        if key >= 0:
            return self.whole[key]
        else:
            return self.fractional[-key - 1]

    def __setitem__(self: DecimalNumber, key: int, value: Digit) -> None:
        if key >= 0:
            self.whole[key] = value
        else:
            self.fractional[-key - 1] = value

    #MARKDOWN_AS_FRAC
    @log_decorator
    def as_fraction(self: DecimalNumber) -> FractionNumber:
        log(f'Converting {self} to fraction number...')
        log_indent()

        log(f'Determining denominator based on length of fractional portion ({self.fractional})...')
        denom = IntegerNumber.from_str('1' + '0' * len(self.fractional.digits))
        log(f'{denom}')

        log(f'Converting fractional portion ({self.fractional} to fraction...')
        fractional_fraction = FractionNumber(
            IntegerNumber.from_str(str(self.fractional)),
            denom
        )
        log(f'{fractional_fraction}')

        log(f'Converting whole portion ({self.whole}) to fraction...')
        whole_fraction = FractionNumber.from_whole(self.whole)
        log(f'{whole_fraction}')

        log(f'Adding ({whole_fraction}) to ({fractional_fraction})...')
        fraction = whole_fraction + fractional_fraction
        log(f'{fraction}')

        log(f'Applying sign of ({self.sign}) to {fraction}...')
        if self.sign == Sign.NEGATIVE:
            fraction = fraction * FractionNumber.from_str("-1/1")  # make sign negative
        log(f'{fraction}')

        log_unindent()

        return fraction
    #MARKDOWN_AS_FRAC

    #MARKDOWN_TO_WORDS
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
    #MARKDOWN_TO_WORDS

    #MARKDOWN_ROUND
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
    #MARKDOWN_ROUND

    #MARKDOWN_EQ
    @log_decorator
    def __eq__(lhs: DecimalNumber, rhs: DecimalNumber) -> bool:
        class FailedTestException(Exception):
            pass

        log(f'Equality testing {lhs} and {rhs}...')
        log_indent()

        try:
            log(f'Testing sign...')
            sign_eq = lhs.sign == rhs.sign
            if not sign_eq:
                raise FailedTestException()
            log(f'Equal')

            log(f'Testing whole...')
            whole_eq = lhs.whole == rhs.whole
            if not whole_eq:
                raise FailedTestException()
            log(f'Equal')

            log(f'Testing fractional...')
            fractional_eq = lhs.fractional == rhs.fractional
            if not fractional_eq:
                raise FailedTestException()
            log(f'Equal')

            ret = True
        except FailedTestException:
            log(f'Not equal')
            ret = False

        log_unindent()
        log(f'{ret}')

        return ret
    #MARKDOWN_EQ

    #MARKDOWN_LT
    @log_decorator
    def __lt__(lhs: DecimalNumber, rhs: DecimalNumber) -> bool:
        class PassedTestException(Exception):
            pass

        class FailedTestException(Exception):
            pass

        log(f'Less than testing {lhs} and {rhs}...')
        log_indent()

        try:
            log(f'Testing sign...')
            sign_lt = (lhs.sign == Sign.NEGATIVE or lhs.sign is None) and rhs.sign == Sign.POSITIVE
            if sign_lt:
                raise PassedTestException()
            sign_eq = lhs.sign == rhs.sign
            if not sign_eq:
                raise FailedTestException()
            log(f'Equal')

            log(f'Testing whole...')
            if lhs.sign != Sign.NEGATIVE:
                whole_lt = lhs.whole < rhs.whole
            else:
                whole_lt = lhs.whole > rhs.whole
            if whole_lt:
                raise PassedTestException()
            whole_eq = lhs.whole == rhs.whole
            if not whole_eq:
                raise FailedTestException()
            log(f'Equal')

            log(f'Testing fractional...')
            if lhs.sign != Sign.NEGATIVE:
                fractional_lt = lhs.fractional < rhs.fractional
            else:
                fractional_lt = lhs.fractional > rhs.fractional
            if fractional_lt:
                raise PassedTestException()
            fractional_eq = lhs.fractional == rhs.fractional
            if not fractional_eq:
                raise FailedTestException()
            log(f'Equal')

            ret = False
        except PassedTestException:
            log(f'Less')
            ret = True
        except FailedTestException:
            log(f'Not less or equal')
            ret = False

        log_unindent()
        log(f'{ret}')

        return ret
    #MARKDOWN_LT

    def __le__(lhs: DecimalNumber, rhs: DecimalNumber) -> bool:
        return lhs < rhs or lhs == rhs

    #MARKDOWN_GT
    @log_decorator
    def __gt__(lhs: DecimalNumber, rhs: DecimalNumber) -> bool:
        class PassedTestException(Exception):
            pass

        class FailedTestException(Exception):
            pass

        log(f'Greater than testing {lhs} and {rhs}...')
        log_indent()

        try:
            log(f'Testing sign...')
            sign_gt = lhs.sign == Sign.POSITIVE and (rhs.sign == Sign.NEGATIVE or rhs.sign is None)
            if sign_gt:
                raise PassedTestException()
            sign_eq = lhs.sign == rhs.sign
            if not sign_eq:
                raise FailedTestException()
            log(f'Equal')

            log(f'Testing whole...')
            if lhs.sign != Sign.NEGATIVE:
                whole_gt = lhs.whole > rhs.whole
            else:
                whole_gt = lhs.whole < rhs.whole
            if whole_gt:
                raise PassedTestException()
            whole_eq = lhs.whole == rhs.whole
            if not whole_eq:
                raise FailedTestException()
            log(f'Equal')

            log(f'Testing fractional...')
            if lhs.sign != Sign.NEGATIVE:
                fractional_gt = lhs.fractional > rhs.fractional
            else:
                fractional_gt = lhs.fractional < rhs.fractional
            if fractional_gt:
                raise PassedTestException()
            fractional_eq = lhs.fractional == rhs.fractional
            if not fractional_eq:
                raise FailedTestException()
            log(f'Equal')

            ret = False
        except PassedTestException:
            log(f'Greater')
            ret = True
        except FailedTestException:
            log(f'Not greater or equal')
            ret = False

        log_unindent()
        log(f'{ret}')

        return ret
    #MARKDOWN_GT

    def __ge__(lhs: DecimalNumber, rhs: DecimalNumber) -> bool:
        return lhs > rhs or lhs == rhs

    #MARKDOWN_ADD
    @log_decorator
    def __add__(lhs: DecimalNumber, rhs: DecimalNumber) -> DecimalNumber:
        log(f'Adding {lhs} and {rhs}...')
        log_indent()

        adjust_len = max(
            len(lhs.fractional.digits),
            len(rhs.fractional.digits)
        )

        log(f'Generating mock integer number for {lhs}...')
        lhs_extra_0s = adjust_len - len(lhs.fractional.digits)
        lhs_combined_digits = lhs.fractional.digits + lhs.whole.digits
        lhs_combined_digits[0:0] = [Digit(0)] * lhs_extra_0s
        mock_self = IntegerNumber(lhs.sign, WholeNumber(lhs_combined_digits))
        log(f'{mock_self}')

        log(f'Generating mock integer number for {rhs}...')
        rhs_extra_0s = adjust_len - len(rhs.fractional.digits)
        rhs_combined_digits = rhs.fractional.digits + rhs.whole.digits
        rhs_combined_digits[0:0] = [Digit(0)] * rhs_extra_0s
        mock_other = IntegerNumber(rhs.sign, WholeNumber(rhs_combined_digits))
        log(f'{mock_other}')

        log(f'Performing {mock_self} + {mock_other}...')
        mock_ret = mock_self + mock_other
        log(f'{mock_ret}')

        log(f'Unmocking {mock_ret} back to decimal...')
        ret_sign = mock_ret.sign
        ret_fractional_digits = [mock_ret.magnitude[i] for i in range(0, adjust_len)]
        ret_whole_digits = [mock_ret.magnitude[i] for i in range(adjust_len, len(mock_ret.magnitude.digits))]
        ret = DecimalNumber(ret_sign, WholeNumber(ret_whole_digits), FractionalNumber(ret_fractional_digits))
        log(f'{ret}')

        log_unindent()
        log(f'{ret}')

        return ret
    #MARKDOWN_ADD

    #MARKDOWN_SUB
    @log_decorator
    def __sub__(lhs: DecimalNumber, rhs: DecimalNumber) -> DecimalNumber:
        log(f'Subtracting {lhs} and {rhs}...')
        log_indent()

        adjust_len = max(
            len(lhs.fractional.digits),
            len(rhs.fractional.digits)
        )

        log(f'Generating mock integer number for {lhs}...')
        lhs_extra_0s = adjust_len - len(lhs.fractional.digits)
        lhs_combined_digits = lhs.fractional.digits + lhs.whole.digits
        lhs_combined_digits[0:0] = [Digit(0)] * lhs_extra_0s
        mock_self = IntegerNumber(lhs.sign, WholeNumber(lhs_combined_digits))
        log(f'{mock_self}')

        log(f'Generating mock integer number for {rhs}...')
        rhs_extra_0s = adjust_len - len(rhs.fractional.digits)
        rhs_combined_digits = rhs.fractional.digits + rhs.whole.digits
        rhs_combined_digits[0:0] = [Digit(0)] * rhs_extra_0s
        mock_other = IntegerNumber(rhs.sign, WholeNumber(rhs_combined_digits))
        log(f'{mock_other}')

        log(f'Performing {mock_self} - {mock_other}...')
        mock_ret = mock_self - mock_other
        log(f'{mock_ret}')

        log(f'Unmocking {mock_ret} back to decimal...')
        ret_sign = mock_ret.sign
        ret_fractional_digits = [mock_ret.magnitude[i] for i in range(0, adjust_len)]
        ret_whole_digits = [mock_ret.magnitude[i] for i in range(adjust_len, len(mock_ret.magnitude.digits))]
        ret = DecimalNumber(ret_sign, WholeNumber(ret_whole_digits), FractionalNumber(ret_fractional_digits))
        log(f'{ret}')

        log_unindent()
        log(f'{ret}')

        return ret
    #MARKDOWN_SUB

    #MARKDOWN_MUL
    @log_decorator
    def __mul__(lhs: DecimalNumber, rhs: DecimalNumber) -> DecimalNumber:
        log(f'Multiplying {lhs} and {rhs}...')
        log_indent()

        adjust_len_self = len(lhs.fractional.digits)
        adjust_len_other = len(rhs.fractional.digits)

        log(f'Generating mock integer number for {lhs}...')
        lhs_extra_0s = adjust_len_self - len(lhs.fractional.digits)
        lhs_combined_digits = lhs.fractional.digits + lhs.whole.digits
        lhs_combined_digits[0:0] = [Digit(0)] * lhs_extra_0s
        mock_self = IntegerNumber(lhs.sign, WholeNumber(lhs_combined_digits))
        log(f'{mock_self}')

        log(f'Generating mock integer number for {rhs}...')
        rhs_extra_0s = adjust_len_other - len(rhs.fractional.digits)
        rhs_combined_digits = rhs.fractional.digits + rhs.whole.digits
        rhs_combined_digits[0:0] = [Digit(0)] * rhs_extra_0s
        mock_other = IntegerNumber(rhs.sign, WholeNumber(rhs_combined_digits))
        log(f'{mock_other}')

        log(f'Performing {mock_self} * {mock_other}...')
        mock_ret = mock_self * mock_other
        log(f'{mock_ret}')

        log(f'Unmocking {mock_ret} back to decimal...')
        unadjust_len = adjust_len_self + adjust_len_other
        ret_sign = mock_ret.sign
        ret_fractional_digits = [mock_ret.magnitude[i] for i in range(0, unadjust_len)]
        ret_whole_digits = [mock_ret.magnitude[i] for i in range(unadjust_len, len(mock_ret.magnitude.digits))]
        ret = DecimalNumber(ret_sign, WholeNumber(ret_whole_digits), FractionalNumber(ret_fractional_digits))
        log(f'{ret}')

        log_unindent()
        log(f'{ret}')

        return ret
    #MARKDOWN_MUL


    #MARKDOWN_DIVTERM_TEST
    @staticmethod
    @log_decorator
    def will_division_terminate(lhs: DecimalNumber, rhs: DecimalNumber) -> bool:
        log(f'Checking if {lhs} / {rhs} results in a non-terminating decimal...')
        log_indent()

        adjust_len_self = len(lhs.fractional.digits)
        adjust_len_other = len(rhs.fractional.digits)

        log(f'Generating mock integer number for {lhs}...')
        lhs_extra_0s = adjust_len_self - len(lhs.fractional.digits)
        lhs_combined_digits = lhs.fractional.digits + lhs.whole.digits
        lhs_combined_digits[0:0] = [Digit(0)] * lhs_extra_0s
        mock_self = IntegerNumber(lhs.sign, WholeNumber(lhs_combined_digits))
        log(f'{mock_self}')

        log(f'Generating mock integer number for {rhs}...')
        rhs_extra_0s = adjust_len_other - len(rhs.fractional.digits)
        rhs_combined_digits = rhs.fractional.digits + rhs.whole.digits
        rhs_combined_digits[0:0] = [Digit(0)] * rhs_extra_0s
        mock_other = IntegerNumber(rhs.sign, WholeNumber(rhs_combined_digits))
        log(f'{mock_other}')

        log(f'Generating mock fraction for {lhs} / {rhs}...')
        mock_fraction = FractionNumber(mock_self, mock_other)
        log(f'{mock_fraction}')

        log(f'Simplifying mock fraction...')
        mock_fraction = mock_fraction.simplify()
        log(f'{mock_fraction}')

        log(f'Checking if prime factors of denom ({mock_fraction.denominator}) is {{}}, {{2}}, {{5}}, or {{2,5}}...')
        mock_fraction_denom_prime_factors = set(factor_tree(mock_fraction.denominator).get_prime_factors())
        if not ({WholeNumber.from_str('2'), WholeNumber.from_str('5')} == mock_fraction_denom_prime_factors
                or {WholeNumber.from_str('2')} == mock_fraction_denom_prime_factors
                or {WholeNumber.from_str('5')} == mock_fraction_denom_prime_factors
                or 0 == len(mock_fraction_denom_prime_factors)):
            ret = False
            log(f'{ret} -- Won\'t terminate.')
        else:
            ret = True
            log(f'{ret} -- Will terminate.')

        log_unindent()
        log(f'{ret}')
        return ret
    #MARKDOWN_DIVTERM_TEST


    #MARKDOWN_DIVTE
    @staticmethod
    @log_decorator
    def choose_start_test_num_for_divte(input1: DecimalNumber, expected_product: DecimalNumber) -> DecimalNumber:
        log(f'Choosing a starting number to find {input1} \\* ? = {expected_product}...')
        log_indent()

        log(f'Checking which case should apply...')
        if input1 < DecimalNumber.from_str('1.0') and expected_product >= DecimalNumber.from_str('1.0'):
            log(f'{input1} has {len(input1.fractional.digits)} fractional digits')
            log(f'{expected_product}\'s has {len(expected_product.whole.digits)} whole digits')
            num_of_zeros = len(expected_product.whole.digits) + len(input1.fractional.digits) - 1
            start_test_num = DecimalNumber.from_str('1' + '0' * num_of_zeros)
        else:
            log(f'{input1} has {len(input1.whole.digits)} whole digits')
            log(f'{expected_product}\'s has {len(expected_product.whole.digits)} whole digits')
            num_of_zeros = len(expected_product.whole.digits) - len(input1.whole.digits)
            start_test_num = DecimalNumber.from_str('1' + '0' * num_of_zeros)

        log(f'Starting number: {start_test_num}')

        log_unindent()
        log(f'{start_test_num}')
        return start_test_num

    @staticmethod
    @log_decorator
    def choose_start_modifier_for_divte(start_test_num: DecimalNumber) -> DecimalNumber:
        log(f'Choosing a starting modifier for {start_test_num}...')
        log_indent()

        log(f'{start_test_num} has {len(start_test_num.whole.digits)} digits')
        num_of_zeros = len(start_test_num.whole.digits) - 1
        start_modifier_num = DecimalNumber.from_str('1' + '0' * num_of_zeros)

        log(f'Starting modifier: {start_modifier_num}')

        log_unindent()
        log(f'{start_modifier_num}')
        return start_modifier_num

    @staticmethod
    @log_decorator
    def trial_and_error_div(dividend: DecimalNumber, divisor: DecimalNumber) -> DecimalNumber:
        log(f'Dividing {dividend} and {divisor}...')
        log_indent()

        log(f'Ensuring {dividend} / {divisor} results in a terminating decimal...')
        if not DecimalNumber.will_division_terminate(dividend, divisor):
            raise Exception('Resulting decimal will be non-terminating')

        log(f'Treating {dividend} and {divisor} as non-negative to perform the algorithm...')
        orig_dividend_sign = dividend.sign
        orig_divisor_sign = divisor.sign
        if dividend.sign == Sign.NEGATIVE:
            dividend *= DecimalNumber.from_str('-1.0')
        if divisor.sign == Sign.NEGATIVE:
            divisor *= DecimalNumber.from_str('-1.0')
        log(f'Non-negative: {dividend} and {divisor}...')

        log(f'Calculating starting test number...')
        test = DecimalNumber.choose_start_test_num_for_divte(divisor, dividend)
        log(f'{test}')

        log(f'Calculating starting modifier for test number...')
        modifier = DecimalNumber.choose_start_modifier_for_divte(test)
        log(f'{modifier}')

        while True:
            log(f'Testing {test}: {test} * {divisor}...')
            test_res = test * divisor
            log(f'{test_res}')

            log(f'Is {test_res} ==, >, or < to {dividend}? ...')
            log_indent()
            try:
                if test_res == dividend:
                    log(f'{test_res} == {dividend} -- Found')
                    break
                elif test_res > dividend:
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

            log(f'Calculating position for next test...')
            modifier *= DecimalNumber.from_str('0.1')
            log(f'{modifier}')

        log_unindent()
        log(f'{test}')

        log(f'Modifying sign of {test} based on original sign of dividend ({orig_dividend_sign}) and divisor ({orig_divisor_sign})...')
        if orig_dividend_sign == Sign.NEGATIVE and orig_divisor_sign != Sign.NEGATIVE \
                or orig_dividend_sign != Sign.NEGATIVE and orig_divisor_sign == Sign.NEGATIVE:
            test *= DecimalNumber.from_str('-1.0')
        log(f'{test}')

        return test
    #MARKDOWN_DIVTE


if __name__ == '__main__':
    # print(f'{DecimalNumber.from_str("1.2").as_fraction()}')
    # print(f'{DecimalNumber.from_str("1.02").as_fraction()}')
    # print(f'{DecimalNumber.from_str("-1.20").as_fraction()}')
    # print(f'{DecimalNumber.from_str("-00.00").as_fraction()}')

    # print(f'{DecimalNumber.from_fraction(FractionNumber.from_str("5/10"))}')
    # print(f'{DecimalNumber.from_fraction(FractionNumber.from_str("-5/10"))}')
    # print(f'{DecimalNumber.from_fraction(FractionNumber.from_str("15/10"))}')
    # print(f'{DecimalNumber.from_fraction(FractionNumber.from_str("-15/10"))}')
    #
    # print('---')
    #
    # print(f'{DecimalNumber.from_fraction(FractionNumber.from_str("1/2"))}')
    # print(f'{DecimalNumber.from_fraction(FractionNumber.from_str("-1/2"))}')
    # print(f'{DecimalNumber.from_fraction(FractionNumber.from_str("3/2"))}')
    # print(f'{DecimalNumber.from_fraction(FractionNumber.from_str("-3/2"))}')
    #
    # print('---')
    #
    # print(f'{DecimalNumber.from_fraction(FractionNumber.from_str("-1/20"))}')
    # print(f'{DecimalNumber.from_fraction(FractionNumber.from_str("-10/200"))}')
    #
    # print('---')
    #
    # print(f'{DecimalNumber.from_fraction(FractionNumber.from_str("-1/30"))}')  # this should fail

    # print(f'{DecimalNumber.from_fraction(FractionNumber.from_str("5/10")).as_fraction()}')
    # print(f'{DecimalNumber.from_fraction(FractionNumber.from_str("-5/10")).as_fraction()}')
    # print(f'{DecimalNumber.from_fraction(FractionNumber.from_str("15/10")).as_fraction()}')
    # print(f'{DecimalNumber.from_fraction(FractionNumber.from_str("-15/10")).as_fraction()}')
    #
    # print('---')
    #
    # print(f'{DecimalNumber.from_fraction(FractionNumber.from_str("1/2")).as_fraction()}')
    # print(f'{DecimalNumber.from_fraction(FractionNumber.from_str("-1/2")).as_fraction()}')
    # print(f'{DecimalNumber.from_fraction(FractionNumber.from_str("3/2")).as_fraction()}')
    # print(f'{DecimalNumber.from_fraction(FractionNumber.from_str("-3/2")).as_fraction()}')
    #
    # print('---')
    #
    # print(f'{DecimalNumber.from_fraction(FractionNumber.from_str("-1/20")).as_fraction()}')
    # print(f'{DecimalNumber.from_fraction(FractionNumber.from_str("-10/200")).as_fraction()}')

    # print(f'{DecimalNumber.from_str("-1.2").to_words()}')
    # print(f'{DecimalNumber.from_str("-1.20").to_words()}')
    # print(f'{DecimalNumber.from_str("-1.02").to_words()}')
    # print(f'{DecimalNumber.from_str("0.1").to_words()}')
    # print(f'{DecimalNumber.from_str("-0.1").to_words()}')
    # print(f'{DecimalNumber.from_str("0.0").to_words()}')
    # print(f'{DecimalNumber.from_str("1.0").to_words()}')

    # print(f'{DecimalNumber.from_str("12.34") == DecimalNumber.from_str("012.340")}')
    # print(f'{DecimalNumber.from_str("12.34") == DecimalNumber.from_str("12.345")}')
    # print(f'{DecimalNumber.from_str("12.34") == DecimalNumber.from_str("112.34")}')
    # print(f'{DecimalNumber.from_str("12.34") == DecimalNumber.from_str("112.345")}')

    # print(f'{DecimalNumber.from_str("0") < DecimalNumber.from_str("0")}')
    # print(f'{DecimalNumber.from_str("0.1") < DecimalNumber.from_str("0")}')
    # print(f'{DecimalNumber.from_str("-0.1") < DecimalNumber.from_str("0")}')
    # print(f'{DecimalNumber.from_str("1.0") < DecimalNumber.from_str("0")}')
    # print(f'{DecimalNumber.from_str("-1.0") < DecimalNumber.from_str("0")}')
    # print(f'{DecimalNumber.from_str("0") < DecimalNumber.from_str("1")}')
    # print(f'{DecimalNumber.from_str("0.1") < DecimalNumber.from_str("1")}')
    # print(f'{DecimalNumber.from_str("-0.1") < DecimalNumber.from_str("1")}')
    # print(f'{DecimalNumber.from_str("1.0") < DecimalNumber.from_str("1")}')
    # print(f'{DecimalNumber.from_str("-1.0") < DecimalNumber.from_str("1")}')
    # print(f'{DecimalNumber.from_str("-2") < DecimalNumber.from_str("-3")}')
    # print(f'{DecimalNumber.from_str("0.4") < DecimalNumber.from_str("0.5")}')
    # print(f'{DecimalNumber.from_str("0.04") < DecimalNumber.from_str("0.05")}')
    # print(f'{DecimalNumber.from_str("0.4") < DecimalNumber.from_str("0.05")}')
    # print(f'{DecimalNumber.from_str("-0.4") < DecimalNumber.from_str("-0.5")}')
    # print(f'{DecimalNumber.from_str("-0.5") < DecimalNumber.from_str("-0.4")}')

    # print(f'{DecimalNumber.from_str("0") > DecimalNumber.from_str("0")}')
    # print(f'{DecimalNumber.from_str("0.1") > DecimalNumber.from_str("0")}')
    # print(f'{DecimalNumber.from_str("-0.1") > DecimalNumber.from_str("0")}')
    # print(f'{DecimalNumber.from_str("1.0") > DecimalNumber.from_str("0")}')
    # print(f'{DecimalNumber.from_str("-1.0") > DecimalNumber.from_str("0")}')
    # print(f'{DecimalNumber.from_str("0") > DecimalNumber.from_str("1")}')
    # print(f'{DecimalNumber.from_str("0.1") > DecimalNumber.from_str("1")}')
    # print(f'{DecimalNumber.from_str("-0.1") > DecimalNumber.from_str("1")}')
    # print(f'{DecimalNumber.from_str("1.0") > DecimalNumber.from_str("1")}')
    # print(f'{DecimalNumber.from_str("-1.0") > DecimalNumber.from_str("1")}')
    # print(f'{DecimalNumber.from_str("-2") > DecimalNumber.from_str("-3")}')
    # print(f'{DecimalNumber.from_str("0.4") > DecimalNumber.from_str("0.5")}')
    # print(f'{DecimalNumber.from_str("0.04") > DecimalNumber.from_str("0.05")}')
    # print(f'{DecimalNumber.from_str("0.4") > DecimalNumber.from_str("0.05")}')
    # print(f'{DecimalNumber.from_str("-0.4") > DecimalNumber.from_str("-0.5")}')
    # print(f'{DecimalNumber.from_str("-0.5") > DecimalNumber.from_str("-0.4")}')

    # print(f'{DecimalNumber.from_str("12.34") + DecimalNumber.from_str("12.34")}')
    # print(f'{DecimalNumber.from_str("0.02") + DecimalNumber.from_str("0.02")}')
    # print(f'{DecimalNumber.from_str("0.02") + DecimalNumber.from_str("0.2")}')
    # print(f'{DecimalNumber.from_str("0.02") + DecimalNumber.from_str("-0.2")}')
    # print(f'{DecimalNumber.from_str("0.02") + DecimalNumber.from_str("-0.02")}')
    # print(f'{DecimalNumber.from_str("0.02") + DecimalNumber.from_str("-0.002")}')
    # print(f'{DecimalNumber.from_str("11.2") + DecimalNumber.from_str("-1.3")}')
    # print(f'{DecimalNumber.from_str("11.2") + DecimalNumber.from_str("1.3")}')
    # print(f'{DecimalNumber.from_str("0.0") + DecimalNumber.from_str("0.0")}')

    # print(f'{DecimalNumber.from_str("12.34") - DecimalNumber.from_str("12.34")}')
    # print(f'{DecimalNumber.from_str("0.02") - DecimalNumber.from_str("0.02")}')
    # print(f'{DecimalNumber.from_str("0.02") - DecimalNumber.from_str("0.2")}')
    # print(f'{DecimalNumber.from_str("0.02") - DecimalNumber.from_str("-0.2")}')
    # print(f'{DecimalNumber.from_str("0.02") - DecimalNumber.from_str("-0.02")}')
    # print(f'{DecimalNumber.from_str("0.02") - DecimalNumber.from_str("-0.002")}')
    # print(f'{DecimalNumber.from_str("11.2") - DecimalNumber.from_str("-1.3")}')
    # print(f'{DecimalNumber.from_str("11.2") - DecimalNumber.from_str("1.3")}')
    # print(f'{DecimalNumber.from_str("0.0") - DecimalNumber.from_str("0.0")}')

    # print(f'{DecimalNumber.from_str("1.111") * DecimalNumber.from_str("2")}')
    # print(f'{DecimalNumber.from_str("2") * DecimalNumber.from_str("1.111")}')
    # print(f'{DecimalNumber.from_str("5.5") * DecimalNumber.from_str("1.1234")}')
    # print(f'{DecimalNumber.from_str("12.34") * DecimalNumber.from_str("12.34")}')
    # print(f'{DecimalNumber.from_str("0.02") * DecimalNumber.from_str("0.02")}')
    # print(f'{DecimalNumber.from_str("0.02") * DecimalNumber.from_str("0.2")}')
    # print(f'{DecimalNumber.from_str("0.02") * DecimalNumber.from_str("-0.2")}')
    # print(f'{DecimalNumber.from_str("0.02") * DecimalNumber.from_str("-0.02")}')
    # print(f'{DecimalNumber.from_str("0.02") * DecimalNumber.from_str("-0.002")}')
    # print(f'{DecimalNumber.from_str("11.2") * DecimalNumber.from_str("-1.3")}')
    # print(f'{DecimalNumber.from_str("11.2") * DecimalNumber.from_str("1.3")}')
    # print(f'{DecimalNumber.from_str("0.0") * DecimalNumber.from_str("0.0")}')

    # print(f'{DecimalNumber.from_str("-271") / DecimalNumber.from_str("-25")}')
    #
    # print(f'{DecimalNumber.from_str("-271") / DecimalNumber.from_str("25")}')
    # print(f'{DecimalNumber.from_str("271") / DecimalNumber.from_str("-2.5")}')
    # print(f'{DecimalNumber.from_str("-27.1") / DecimalNumber.from_str("2.5")}')
    # print(f'{DecimalNumber.from_str("2.71") / DecimalNumber.from_str("-2.5")}')
    # print(f'{DecimalNumber.from_str("-271") / DecimalNumber.from_str("0.25")}')
    # print(f'{DecimalNumber.from_str("0") / DecimalNumber.from_str("-25")}')
    #
    # print(f'{DecimalNumber.from_str("271") / DecimalNumber.from_str("25")}')
    # print(f'{DecimalNumber.from_str("271") / DecimalNumber.from_str("2.5")}')
    # print(f'{DecimalNumber.from_str("27.1") / DecimalNumber.from_str("2.5")}')
    # print(f'{DecimalNumber.from_str("2.71") / DecimalNumber.from_str("2.5")}')
    # print(f'{DecimalNumber.from_str("271") / DecimalNumber.from_str("0.25")}')
    # print(f'{DecimalNumber.from_str("0") / DecimalNumber.from_str("25")}')

    # log_whitelist([(inspect.getfile(DecimalNumber), '__truediv__')])
    # print(f'{DecimalNumber.from_str("21") / DecimalNumber.from_str("4")}')

    log_whitelist([(inspect.getfile(DecimalNumber), 'trial_and_error_div')])
    print(f'{DecimalNumber.trial_and_error_div(DecimalNumber.from_str("11"), DecimalNumber.from_str("2"))}')

    # print(f'{DecimalNumber.from_str("123.456")[3]}')
    # print(f'{DecimalNumber.from_str("123.456")[2]}')
    # print(f'{DecimalNumber.from_str("123.456")[1]}')
    # print(f'{DecimalNumber.from_str("123.456")[0]}')
    # print(f'{DecimalNumber.from_str("123.456")[-1]}')
    # print(f'{DecimalNumber.from_str("123.456")[-2]}')
    # print(f'{DecimalNumber.from_str("123.456")[-3]}')
    # print(f'{DecimalNumber.from_str("123.456")[-4]}')

    # print(f'{DecimalNumber.from_str("123.456").round(3)}')
    # print(f'{DecimalNumber.from_str("123.456").round(2)}')
    # print(f'{DecimalNumber.from_str("123.456").round(1)}')
    # print(f'{DecimalNumber.from_str("123.456").round(0)}')
    # print(f'{DecimalNumber.from_str("123.456").round(-1)}')
    # print(f'{DecimalNumber.from_str("123.456").round(-2)}')
    # print(f'{DecimalNumber.from_str("123.456").round(-3)}')
    # print(f'{DecimalNumber.from_str("123.456").round(-4)}')
    #
    # print(f'{DecimalNumber.from_str("456.123").round(3)}')
    # print(f'{DecimalNumber.from_str("456.123").round(2)}')
    # print(f'{DecimalNumber.from_str("456.123").round(1)}')
    # print(f'{DecimalNumber.from_str("456.123").round(0)}')
    # print(f'{DecimalNumber.from_str("456.123").round(-1)}')
    # print(f'{DecimalNumber.from_str("456.123").round(-2)}')
    # print(f'{DecimalNumber.from_str("456.123").round(-3)}')
    # print(f'{DecimalNumber.from_str("456.123").round(-4)}')
    #
    # print(f'{DecimalNumber.from_str("999.999").round(4)}')
    # print(f'{DecimalNumber.from_str("999.999").round(3)}')
    # print(f'{DecimalNumber.from_str("999.999").round(2)}')
    # print(f'{DecimalNumber.from_str("999.999").round(1)}')
    # print(f'{DecimalNumber.from_str("999.999").round(0)}')
    # print(f'{DecimalNumber.from_str("999.999").round(-1)}')
    # print(f'{DecimalNumber.from_str("999.999").round(-2)}')
    # print(f'{DecimalNumber.from_str("999.999").round(-3)}')
    # print(f'{DecimalNumber.from_str("999.999").round(-4)}')
    pass