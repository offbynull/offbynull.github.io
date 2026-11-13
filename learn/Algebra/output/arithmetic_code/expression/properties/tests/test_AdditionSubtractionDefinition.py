import unittest

from expression.parser.Parser import parse
from expression.conversions.AdditionSubtractionConversion import add_to_sub, sub_to_add


class Test(unittest.TestCase):
    def test_must_convert_add_to_sub(self):
        actual = add_to_sub(parse('-2+x'))
        expected = {parse('-2-(-x)')}
        self.assertEqual(expected, actual)

    def test_must_convert_sub_to_add(self):
        actual = sub_to_add(parse('-2-x'))
        expected = {parse('-2+(-x)')}
        self.assertEqual(expected, actual)

    def test_must_ignore_single(self):
        self.assertEqual(set(), add_to_sub(parse('-2')))
        self.assertEqual(set(), sub_to_add(parse('-2')))

    def test_must_ignore_other_operator(self):
        self.assertEqual(set(), add_to_sub(parse('x*y')))
        self.assertEqual(set(), sub_to_add(parse('x*y')))

