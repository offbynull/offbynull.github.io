from unittest import TestCase

from expression.parser.Parser import parse
from expression.properties.ExponentPowerProperty import exponent_power, unexponent_power


class Test(TestCase):
    def test_must_flatten_power_of_power(self):
        actual = exponent_power(parse('(x^3)^x'))
        expected = {parse('x^(3*x)')}
        self.assertEqual(expected, actual)

    def test_must_convert_to_power_of_power(self):
        actual = unexponent_power(parse('x^(3*x)'))
        expected = {parse('(x^3)^x')}
        self.assertEqual(expected, actual)

    def test_must_ignore_unknown_operator(self):
        self.assertEqual(set(), exponent_power(parse('(x*3)^x')))
        self.assertEqual(set(), exponent_power(parse('(x^3)*x')))
        self.assertEqual(set(), unexponent_power(parse('x^(3^x)')))
        self.assertEqual(set(), unexponent_power(parse('x*(3^x)')))

    def test_must_ignore_single(self):
        self.assertEqual(set(), exponent_power(parse('-2')))
        self.assertEqual(set(), unexponent_power(parse('-2')))
