from unittest import TestCase

from expression.parser.Parser import parse
from expression.properties.ExponentProductProperty import exponent_product, unexponent_product


class Test(TestCase):
    def test_must_contract(self):
        actual = exponent_product(parse('(x^3)*(x^x)'))
        expected = {parse('x^(3+x)')}
        self.assertEqual(expected, actual)

    def test_must_expand(self):
        actual = unexponent_product(parse('x^(3+x)'))
        expected = {parse('(x^3)*(x^x)')}
        self.assertEqual(expected, actual)

    def test_must_ignore_unknown_operator(self):
        self.assertEqual(set(), exponent_product(parse('(x^3)/(x^x)')))
        self.assertEqual(set(), exponent_product(parse('(x*3)*(x*x)')))
        self.assertEqual(set(), unexponent_product(parse('x^(3*x)')))
        self.assertEqual(set(), unexponent_product(parse('x*(3+x)')))

    def test_must_ignore_single(self):
        self.assertEqual(set(), exponent_product(parse('-2')))
        self.assertEqual(set(), unexponent_product(parse('-2')))
