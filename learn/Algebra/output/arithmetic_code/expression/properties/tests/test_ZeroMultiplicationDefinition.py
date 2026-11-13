from unittest import TestCase

from expression.parser.Parser import parse
from expression.properties.ZeroMultiplicationDefinition import zero_multiplication


class Test(TestCase):
    def test_must_convert_from_zero_mul(self):
        self.assertEqual({parse('0')}, zero_multiplication(parse('x*0')))
