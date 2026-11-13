from unittest import TestCase

from expression.parser.Parser import parse
from expression.properties.ZeroDivisionDefinition import zero_division


class Test(TestCase):
    def test_must_convert_from_zero_div(self):
        self.assertEqual({parse('0')}, zero_division(parse('0/x')))
