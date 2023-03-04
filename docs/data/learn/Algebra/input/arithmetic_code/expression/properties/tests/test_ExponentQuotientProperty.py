from unittest import TestCase

from expression.parser.Parser import parse
from expression.properties.ExponentQuotientProperty import exponent_quotient, unexponent_quotient


class Test(TestCase):
    def test_must_contract(self):
        actual = exponent_quotient(parse('(x^z)/(x^2)'))
        expected = {parse('x^(z-2)')}
        self.assertEqual(expected, actual)

    def test_must_expand(self):
        actual = unexponent_quotient(parse('x^(z-2)'))
        expected = {parse('(x^z)/(x^2)')}
        self.assertEqual(expected, actual)

    def test_must_ignore_unknown_operator(self):
        self.assertEqual(set(), exponent_quotient(parse('(x^z)*(x^2)')))
        self.assertEqual(set(), exponent_quotient(parse('(x*z)/(x*2)')))
        self.assertEqual(set(), unexponent_quotient(parse('x^(z/2)')))
        self.assertEqual(set(), unexponent_quotient(parse('x/(z-2)')))

    def test_must_ignore_single(self):
        self.assertEqual(set(), exponent_quotient(parse('-2')))
        self.assertEqual(set(), unexponent_quotient(parse('-2')))
