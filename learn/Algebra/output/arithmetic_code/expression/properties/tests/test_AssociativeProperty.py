from unittest import TestCase

from expression.parser.Parser import parse
from expression.properties.AssociativeProperty import associative


class Test(TestCase):
    def test_must_swap_inner_operator_to_rhs(self):
        actual = associative(parse('(x*y)*z'))
        expected = {parse('x*(y*z)')}
        self.assertEqual(expected, actual)
        actual = associative(parse('(x+y)+z'))
        expected = {parse('x+(y+z)')}
        self.assertEqual(expected, actual)

    def test_must_swap_inner_operator_to_lhs(self):
        actual = associative(parse('x*(y*z)'))
        expected = {parse('(x*y)*z')}
        self.assertEqual(expected, actual)
        actual = associative(parse('x+(y+z)'))
        expected = {parse('(x+y)+z')}
        self.assertEqual(expected, actual)

    def test_must_ignore_unknown_operator(self):
        self.assertEqual(set(), associative(parse('x/(y/z)')))
        self.assertEqual(set(), associative(parse('x/(y/z)')))

    def test_must_ignore_single(self):
        self.assertEqual(set(), associative(parse('-2')))
