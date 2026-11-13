import inspect
import sys
from pathlib import Path
from sys import stdin

import yaml

import expression.parser.Parser
from expression.Exploder import ExplosionCache, simplify
from expression.Node import Node, FunctionNode, ConstantNode, VariableNode
from relation.Relation import Relation, RelationWithDomain, opposite
from relation.parser.Parser import parse
from relation.parser.Printer import to_string


# MARKDOWN_ADD
def addition(rel: Relation, operand: Node, cache: ExplosionCache) -> set[RelationWithDomain]:
    if rel.op == '>=':
        _lhs = FunctionNode('+', [rel.lhs, operand])
        _rhs = FunctionNode('+', [rel.rhs, operand])
        return {RelationWithDomain.create(rel.op, _lhs, _rhs)}
    return set()
# MARKDOWN_ADD

# MARKDOWN_SUB
def subtraction(rel: Relation, operand: Node, cache: ExplosionCache) -> set[RelationWithDomain]:
    if rel.op == '>=':
        _lhs = FunctionNode('-', [rel.lhs, operand])
        _rhs = FunctionNode('-', [rel.rhs, operand])
        return {RelationWithDomain.create(rel.op, _lhs, _rhs)}
    return set()
# MARKDOWN_SUB

# MARKDOWN_MUL
def multiplication(rel: Relation, operand: Node, cache: ExplosionCache) -> set[RelationWithDomain]:
    if rel.op == '>=':
        operand, _ = simplify(operand, cache)
        if isinstance(operand, ConstantNode):
            _lhs = FunctionNode('*', [rel.lhs, operand])
            _rhs = FunctionNode('*', [rel.rhs, operand])
            if operand >= 0:
                return {RelationWithDomain.create(rel.op, _lhs, _rhs)}
            else:
                return {RelationWithDomain.create(opposite(rel.op), _lhs, _rhs)}
        else:
            _lhs = FunctionNode('*', [rel.lhs, operand])
            _rhs = FunctionNode('*', [rel.rhs, operand])
            return {
                RelationWithDomain.create(
                    rel.op,
                    _lhs,
                    _rhs,
                    {Relation('>', operand, ConstantNode(0))}
                ),
                RelationWithDomain.create(
                    opposite(rel.op),
                    _lhs,
                    FunctionNode('*', [ConstantNode(-1), _rhs]),
                    {Relation('<=', operand, ConstantNode(0))}
                )
            }
    return set()
# MARKDOWN_MUL

# MARKDOWN_DIV
def division(rel: Relation, operand: Node, cache: ExplosionCache) -> set[RelationWithDomain]:
    if rel.op == '>=':
        operand, _ = simplify(operand, cache)
        if isinstance(operand, ConstantNode):
            _lhs = FunctionNode('*', [rel.lhs, operand])
            _rhs = FunctionNode('*', [rel.rhs, operand])
            if operand >= 0:
                return {RelationWithDomain.create(rel.op, _lhs, _rhs)}
            else:
                return {RelationWithDomain.create(opposite(rel.op), _lhs, _rhs)}
        else:
            _lhs = FunctionNode('/', [rel.lhs, operand])
            _rhs = FunctionNode('/', [rel.rhs, operand])
            return {
                RelationWithDomain.create(
                    rel.op,
                    _lhs,
                    _rhs,
                    {Relation('>', operand, ConstantNode(0))}
                ),
                RelationWithDomain.create(
                    opposite(rel.op),
                    _lhs,
                    FunctionNode('*', [ConstantNode(-1), _rhs]),
                    {Relation('<=', operand, ConstantNode(0))}
                )
            }
    return set()
# MARKDOWN_DIV


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    funcs = {n: o for n, o in inspect.getmembers(sys.modules[__name__]) if (inspect.isfunction(o) and n != 'main')}
    try:
        data_raw = ''.join(stdin.readlines())
        data: list = yaml.safe_load(data_raw)
        print(f'{Path(__file__).name} produced the following alternate forms ...')
        print()
        # print('```')
        # print(data_raw)
        # print('```')
        # print()
        # print(f'The following alternative forms were produced ...')
        # print()
        print('```')
        for func_name, rel, operand in data:
            rel = parse(str(rel))
            operand = expression.parser.Parser.parse(str(operand))
            func = funcs[func_name]
            print(f'{func_name} with input {to_string(rel), expression.parser.Printer.to_string(operand)} ...')
            for alt_rel in func(rel, operand, ExplosionCache()):
                print(f'    {to_string(alt_rel)}')
        print('```')
        print()
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    r = parse('x+1<5')
    for _r in addition(r, VariableNode('x'), ExplosionCache()):
        print(f'{to_string(r)} ⟶ {to_string(_r)}')
    for _r in subtraction(r, VariableNode('x'), ExplosionCache()):
        print(f'{to_string(r)} ⟶ {to_string(_r)}')
    for _r in multiplication(r, VariableNode('x'), ExplosionCache()):
        print(f'{to_string(r)} ⟶ {to_string(_r)}')
    for _r in division(r, VariableNode('x'), ExplosionCache()):
        print(f'{to_string(r)} ⟶ {to_string(_r)}')
