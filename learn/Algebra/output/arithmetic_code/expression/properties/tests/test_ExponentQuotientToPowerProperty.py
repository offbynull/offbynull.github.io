from unittest import TestCase

from expression.parser.Parser import parse
from expression.properties.ExponentQuotientToPowerProperty import exponent_quotient_to_power, \
    unexponent_quotient_to_power


class Test(TestCase):
    def test_must_expand(self):
        actual = exponent_quotient_to_power(parse('(x/y)^3'))
        expected = {parse('(x^3)/(y^3)')}
        self.assertEqual(expected, actual)

    def test_must_contract(self):
        actual = unexponent_quotient_to_power(parse('(x^3)/(y^3)'))
        expected = {parse('(x/y)^3')}
        self.assertEqual(expected, actual)

    def test_must_ignore_unknown_operator(self):
        self.assertEqual(set(), exponent_quotient_to_power(parse('(x*y)^3')))
        self.assertEqual(set(), exponent_quotient_to_power(parse('(x/y)/3')))
        self.assertEqual(set(), unexponent_quotient_to_power(parse('(x*3)/(y*3)')))
        self.assertEqual(set(), unexponent_quotient_to_power(parse('(x^3)*(y^3)')))

    def test_must_ignore_single(self):
        self.assertEqual(set(), exponent_quotient_to_power(parse('-2')))
        self.assertEqual(set(), unexponent_quotient_to_power(parse('-2')))
