from unittest import TestCase

from expression.parser.Parser import parse
from expression.properties.OneExponentDefinition import from_one_exponent, to_one_exponent


class Test(TestCase):
    def test_must_convert_from_one_exp(self):
        self.assertEqual({parse('x')}, from_one_exponent(parse('x^1')))

    def test_must_convert_to_one_exp(self):
        self.assertEqual({parse('x^1')}, to_one_exponent(parse('x')))
