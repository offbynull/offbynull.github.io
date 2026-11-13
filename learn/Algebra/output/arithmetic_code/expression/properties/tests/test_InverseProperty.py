from unittest import TestCase

from expression.parser.Parser import parse
from expression.properties.InverseProperty import inverse


class Test(TestCase):
    def test_must_swallow_inverse(self):
        self.assertEqual({parse('1')}, inverse(parse('x/x')))
        self.assertEqual({parse('0')}, inverse(parse('x-x')))
        self.assertEqual({parse('0')}, inverse(parse('x+-x')))
        self.assertEqual({parse('1')}, inverse(parse('x*(1/x)')))

    def test_must_ignore_unknown_operator(self):
        self.assertEqual(set(), inverse(parse('x*x')))

    def test_must_ignore_single(self):
        self.assertEqual(set(), inverse(parse('-2')))
        self.assertEqual(set(), inverse(parse('-2')))
