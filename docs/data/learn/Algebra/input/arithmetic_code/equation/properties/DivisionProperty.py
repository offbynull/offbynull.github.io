from itertools import product

from equation.Equality import Equality
from expression.Exploder import explode, ExplosionCache
from expression.Utils import extract_all
from expression.parser.Parser import FunctionNode, parse


def division(eq: Equality, cache: ExplosionCache) -> set[Equality]:
    options = {eq}
    for operand in extract_all(eq.lhs) | extract_all(eq.rhs):
        if operand == 0:
            continue
        _lhs = FunctionNode('/', [eq.lhs, operand])
        _rhs = FunctionNode('/', [eq.rhs, operand])
        for _lhs, _rhs in product(explode(_lhs, cache), explode(_rhs, cache)):
            options.add(Equality(_lhs, _rhs))
        _lhs = FunctionNode('/', [operand, eq.lhs])
        _rhs = FunctionNode('/', [operand, eq.rhs])
        for _lhs, _rhs in product(explode(_lhs, cache), explode(_rhs, cache)):
            options.add(Equality(_lhs, _rhs))
    return options


if __name__ == '__main__':
    eq = Equality(parse('2*x'), parse('4'))
    options = division(eq, ExplosionCache())
    for _eq in options:
        print(f'{_eq}')
