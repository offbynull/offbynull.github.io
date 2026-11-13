from unittest import TestCase

from expression.parser.Parser import parse
from expression.properties.ZeroExponentDefinition import zero_exponent


class Test(TestCase):
    def test_must_convert_from_zero_exp(self):
        self.assertEqual({parse('1')}, zero_exponent(parse('x^0')))
