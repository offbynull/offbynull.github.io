import inspect
import sys
from pathlib import Path
from sys import stdin

import yaml

from Factor import factor_fastest
from expression.Node import Node, ConstantNode, FunctionNode
from expression.Utils import top, bottom
from expression.parser.Parser import parse
from expression.parser.Printer import to_string


# MARKDOWN_IDENTITY
def identity(n: Node):
    if not isinstance(n, FunctionNode):
        return set()
    if n.op == '/' and n.args[1] == 1:
        return {n.args[0]}
    return set()
# MARKDOWN_IDENTITY


# MARKDOWN_INVERSE
def inverse(n: Node):
    if not isinstance(n, FunctionNode):
        return set()
    if n.op == '/':
        if n.args[0] == n.args[1] and n.args[1] != 0:
            return {ConstantNode(1)}
    return set()
# MARKDOWN_INVERSE


# MARKDOWN_ZERO
def zero(n: Node):
    if isinstance(n, FunctionNode) and n.op == '/':
        l_arg = n.args[0]
        if l_arg == 0:
            return {ConstantNode(0)}
    return set()
# MARKDOWN_ZERO


def evaluate(n: Node):
    def _to_factors(v):
        if v > 0:
            return factor_fastest(v)
        elif v < 0:
            return factor_fastest(-v)
        else:
            return set()

    if not isinstance(n, FunctionNode):
        return set()
    if n.op == '/':
        l_arg, r_arg = n.args
        if isinstance(l_arg, ConstantNode) and isinstance(r_arg, ConstantNode) and r_arg != 0:
            factors1 = _to_factors(l_arg.value)
            factors2 = _to_factors(r_arg.value)
            factor = max(factors1 & factors2, default=0)
            if factor == 0:
                return set()
            l_arg = l_arg // factor
            r_arg = r_arg // factor
            if r_arg == 1 or r_arg == -1:
                return {l_arg // r_arg}
            else:
                return {FunctionNode('/', [l_arg, r_arg])}
    return set()


# MARKDOWN_COMBINE
def combine(n: Node):
    if not isinstance(n, FunctionNode):
        return set()
    if n.op == '/':
        l_arg, r_arg = n.args
        ret = FunctionNode('/', [
            FunctionNode('*', [top(l_arg), bottom(r_arg)]),
            FunctionNode('*', [bottom(l_arg), top(r_arg)])
        ])
        return {ret}
    return set()


def uncombine(n: Node):
    if not isinstance(n, FunctionNode):
        return set()
    if n.op == '/':
        n_top = top(n)
        n_bottom = bottom(n)
        if not (isinstance(n_top, FunctionNode) and n_top.op == '*'
                and isinstance(n_bottom, FunctionNode) and n_bottom.op == '*'):
            return set()
        l_top, r_top = n_top.args
        l_bottom, r_bottom = n_bottom.args
        ret = FunctionNode('/', [
            FunctionNode('/', [l_top, l_bottom]),
            FunctionNode('/', [r_bottom, r_top])
        ])
        return {ret}
    return set()
# MARKDOWN_COMBINE


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


if __name__ == '__main__':
    for r in combine(parse('a/b')):
        print(f'{to_string(r)}')
    for r in combine(parse('(a/2)/b')):
        print(f'{to_string(r)}')
    for r in combine(parse('(a/b)/(c/d)')):
        print(f'{to_string(r)}')
    for r in combine(parse('(a/3)/(5/1)')):
        print(f'{to_string(r)}')

    for r in uncombine(parse('(a*d)/(b*c)')):
        print(f'{to_string(r)}')
    for r in uncombine(parse('(a*1)/(2*b)')):
        print(f'{to_string(r)}')

    for r in evaluate(parse('5/10')):
        print(f'{to_string(r)}')
    for r in evaluate(parse('-5/10')):
        print(f'{to_string(r)}')
    for r in evaluate(parse('-10/5')):
        print(f'{to_string(r)}')
    for r in evaluate(parse('10/-5')):
        print(f'{to_string(r)}')