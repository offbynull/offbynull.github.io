from itertools import product

from expression.Rearranger import rearrange
from expression.Utils import extract_all
from expression.parser.Parser import FunctionNode, parse, Node
from expression.parser.Printer import to_string


def subtraction(lhs: Node, rhs: Node) -> set[tuple[Node, Node]]:
    options = {(lhs, rhs)}
    for operand in extract_all(lhs) | extract_all(rhs):
        _lhs = FunctionNode('-', [lhs, operand])
        _rhs = FunctionNode('-', [rhs, operand])
        for _lhs, _rhs in product(rearrange(_lhs), rearrange(_rhs)):
            options.add((_lhs, _rhs))
        _lhs = FunctionNode('-', [operand, lhs])
        _rhs = FunctionNode('-', [operand, rhs])
        for _lhs, _rhs in product(rearrange(_lhs), rearrange(_rhs)):
            options.add((_lhs, _rhs))
    return options


if __name__ == '__main__':
    lhs, rhs = parse('x+2'), parse('0')
    options = subtraction(lhs, rhs)
    for _lhs, _rhs in options:
        print(f'{to_string(_lhs)} = {to_string(_rhs)}')
