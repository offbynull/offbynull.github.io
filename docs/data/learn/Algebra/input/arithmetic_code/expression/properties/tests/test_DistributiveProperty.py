from unittest import TestCase

from expression.parser.Parser import parse
from expression.properties.DistributiveProperty import distributive, undistributive


class Test(TestCase):
    def test_must_distribute(self):
        actual = distributive(parse('(x+y)*3'))
        expected = {parse('(x*3)+(y*3)')}
        self.assertEqual(expected, actual)

    def test_must_undistribute(self):
        actual = undistributive(parse('(x*3)+(y*3)'))
        expected = {parse('(x+y)*3')}
        self.assertEqual(expected, actual)

    def test_must_ignore_unknown_operator(self):
        self.assertEqual(set(), distributive(parse('(x+y+1)/3')))
        self.assertEqual(set(), distributive(parse('(x/y/1)*3')))
        self.assertEqual(set(), undistributive(parse('(x*3)/(y*3)')))
        self.assertEqual(set(), undistributive(parse('(x/3)+(y/3)')))

    def test_must_ignore_single(self):
        self.assertEqual(set(), distributive(parse('-2')))
        self.assertEqual(set(), undistributive(parse('-2')))
