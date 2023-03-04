import inspect
import sys
from pathlib import Path
from sys import stdin

import yaml

from expression.Node import Node, ConstantNode, FunctionNode
from expression.Utils import top, bottom
from expression.parser.Parser import parse
from expression.parser.Printer import to_string


# MARKDOWN_COMMUTATIVE
def commutative(n: Node):
    if not isinstance(n, FunctionNode):
        return set()
    variations = set()
    if n.op == '+':
        _n = FunctionNode(
            n.op,
            n.args[::-1]
        )
        variations.add(_n)
    return variations
# MARKDOWN_COMMUTATIVE


# MARKDOWN_ASSOCIATIVE
def associative(n: Node):
    if not isinstance(n, FunctionNode):
        return set()
    variations = set()
    if n.op == '+':
        l_arg = n.args[0]
        r_arg = n.args[1]
        if isinstance(l_arg, FunctionNode) and l_arg.op == n.op:
            _n = FunctionNode(
                n.op,
                [
                    l_arg.args[0],
                    FunctionNode(n.op, [l_arg.args[1], r_arg])
                ]
            )
            variations.add(_n)
        if isinstance(r_arg, FunctionNode) and r_arg.op == n.op:
            _n = FunctionNode(
                n.op,
                [
                    FunctionNode(n.op, [l_arg, r_arg.args[0]]),
                    r_arg.args[1]
                ]
            )
            variations.add(_n)
    return variations
# MARKDOWN_ASSOCIATIVE


# MARKDOWN_IDENTITY
def identity(n: Node):
    if not isinstance(n, FunctionNode):
        return set()
    if n.op == '+' and n.args[1] == 0:
        return {n.args[0]}
    return set()
# MARKDOWN_IDENTITY


# MARKDOWN_INVERSE
def inverse(n: Node):
    if not isinstance(n, FunctionNode):
        return set()
    if n.op == '+':
        if (isinstance(n.args[0], ConstantNode) and n.args[1] == -n.args[0])\
                or n.args[1] == FunctionNode('*', [ConstantNode(-1), n.args[0]]):
            return {ConstantNode(0)}
    return set()
# MARKDOWN_INVERSE


# MARKDOWN_COMBINE
def combine(n: Node):
    if not isinstance(n, FunctionNode):
        return set()
    if n.op == '+':
        l_arg, r_arg = n.args
        ret = FunctionNode('/', [
            FunctionNode(
                '+',
                [
                    FunctionNode('*', [top(l_arg), bottom(r_arg)]),
                    FunctionNode('*', [top(r_arg), bottom(l_arg)])
                ]
            ),
            FunctionNode('*', [bottom(l_arg), bottom(r_arg)])
        ])
        return {ret}
    return set()


def uncombine(n: Node):
    if not isinstance(n, FunctionNode):
        return set()
    n_top = top(n)
    n_bottom = bottom(n)
    if isinstance(n_top, FunctionNode) and n_top.op == '+':
        l_arg = n_top.args[0]
        r_arg = n_top.args[1]
        ret = FunctionNode('+', [
            FunctionNode('/', [l_arg, n_bottom]),
            FunctionNode('/', [r_arg, n_bottom])
        ])
        return {ret}
    return set()
# MARKDOWN_COMBINE


def evaluate(n: Node):
    if not isinstance(n, FunctionNode):
        return set()
    if n.op == '+':
        l_arg, r_arg = n.args
        if isinstance(l_arg, ConstantNode) and isinstance(r_arg, ConstantNode):
            return {ConstantNode(l_arg.value + r_arg.value)}
    return set()


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
        for func_name, exp in data:
            exp = str(exp)
            n = parse(exp)
            func = funcs[func_name]
            print(f'{func_name} with input {exp} ...')
            for alt_n in func(n):
                print(f'    {to_string(n)} = {to_string(alt_n)}')
        print('```')
        print()
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")
