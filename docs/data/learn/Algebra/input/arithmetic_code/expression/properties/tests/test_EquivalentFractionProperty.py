from unittest import TestCase

from expression.parser.Parser import parse
from expression.properties.EquivalentFractionProperty import equivalent_fraction, unequivalent_fraction


class Test(TestCase):
    def test_must_break_apart(self):
        actual = equivalent_fraction(parse('(x*c)/(y*c)'))
        expected = {parse('(x/y)*(c/c)')}
        self.assertEqual(expected, actual)

    def test_must_merge_together(self):
        actual = unequivalent_fraction(parse('(x/y)*(c/c)'))
        expected = {parse('(x*c)/(y*c)')}
        self.assertEqual(expected, actual)

    def test_must_ignore_unknown_operator(self):
        self.assertEqual(set(), equivalent_fraction(parse('(x/c)/(y/c)')))
        self.assertEqual(set(), equivalent_fraction(parse('(x*c)*(y*c)')))
        self.assertEqual(set(), unequivalent_fraction(parse('(x*y)*(c*c)')))
        self.assertEqual(set(), unequivalent_fraction(parse('(x/y)/(c/c)')))

    def test_must_ignore_single(self):
        self.assertEqual(set(), equivalent_fraction(parse('-2')))
        self.assertEqual(set(), unequivalent_fraction(parse('-2')))
