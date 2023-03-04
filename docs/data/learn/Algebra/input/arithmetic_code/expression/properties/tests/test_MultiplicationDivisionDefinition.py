import unittest

from expression.parser.Parser import parse
from expression.properties.MultiplicationDivisionDefinition import mul_to_div, div_to_mul


class Test(unittest.TestCase):
    def test_must_convert_mul_to_div(self):
        actual = mul_to_div(parse('x*y'))
        expected = {parse('(x/1)*(y/1)')}
        self.assertEqual(expected, actual)

    def test_must_convert_div_to_mul(self):
        actual = div_to_mul(parse('x/y'))
        expected = {parse('(x/1)*(1/y)')}
        self.assertEqual(expected, actual)

    def test_must_ignore_single(self):
        self.assertEqual(set(), mul_to_div(parse('-2')))
        self.assertEqual(set(), div_to_mul(parse('-2')))

    def test_must_ignore_other_operator(self):
        self.assertEqual(set(), mul_to_div(parse('x-y')))
        self.assertEqual(set(), div_to_mul(parse('x-y')))

