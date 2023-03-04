from unittest import TestCase

from expression.parser.Parser import parse
from expression.properties.CommutativeProperty import commutative


class Test(TestCase):
    def test_must_swap_operands(self):
        actual = commutative(parse('(x*y)*z'))
        expected = {parse('z*(x*y)')}
        self.assertEqual(expected, actual)
        actual = commutative(parse('(x+y)+z'))
        expected = {parse('z+(x+y)')}
        self.assertEqual(expected, actual)

    def test_must_ignore_unknown_operator(self):
        self.assertEqual(set(), commutative(parse('x/(y/z)')))
        self.assertEqual(set(), commutative(parse('x/(y/z)')))

    def test_must_ignore_single(self):
        self.assertEqual(set(), commutative(parse('-2')))
