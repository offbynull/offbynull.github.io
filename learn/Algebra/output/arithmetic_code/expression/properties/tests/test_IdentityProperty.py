from unittest import TestCase

from expression.parser.Parser import parse
from expression.properties.IdentityProperty import identity


class Test(TestCase):
    def test_must_swallow_identity(self):
        self.assertEqual({parse('x')}, identity(parse('x*1')))
        self.assertEqual({parse('x')}, identity(parse('x/1')))
        self.assertEqual({parse('x')}, identity(parse('x+0')))
        self.assertEqual({parse('x')}, identity(parse('x-0')))

    def test_must_ignore_unknown_operator(self):
        self.assertEqual(set(), identity(parse('x^0')))

    def test_must_ignore_single(self):
        self.assertEqual(set(), identity(parse('-2')))
        self.assertEqual(set(), identity(parse('-2')))
