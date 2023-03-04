from unittest import TestCase

from expression.parser.Parser import parse
from expression.properties.NegativeExponentDefinition import from_negative_exponent, to_negative_exponent


class Test(TestCase):
    def test_must_convert_from_negative_exp(self):
        self.assertEqual({parse('1/(x^y)')}, from_negative_exponent(parse('x^(-y)')))
        self.assertEqual({parse('1/(x^5)')}, from_negative_exponent(parse('x^(-5)')))

    def test_must_convert_to_negative_exp(self):
        self.assertEqual({parse('x^(-y)')}, to_negative_exponent(parse('1/(x^y)')))
        self.assertEqual({parse('x^(-5)')}, to_negative_exponent(parse('1/(x^5)')))

    def test_must_ignore_unknown_operator(self):
        self.assertEqual(set(), from_negative_exponent(parse('x^x')))
        self.assertEqual(set(), to_negative_exponent(parse('1/(x*x)')))

    def test_must_ignore_single(self):
        self.assertEqual(set(), from_negative_exponent(parse('-2')))
        self.assertEqual(set(), to_negative_exponent(parse('-2')))
