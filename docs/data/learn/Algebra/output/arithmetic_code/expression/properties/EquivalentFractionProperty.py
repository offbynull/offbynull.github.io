import inspect
import sys
from pathlib import Path
from sys import stdin

import yaml

from Factor import factor_fastest
from expression.Node import Node, ConstantNode, FunctionNode
from expression.parser.Parser import parse
from expression.parser.Printer import to_string


def equivalent_fraction(n: Node):
    return equivalent_fraction_basic(n) | equivalent_fraction_constant_shortcircuit(n)\
        | equivalent_fraction_exponent_shortcircuit(n)


# MARKDOWN
def equivalent_fraction_basic(n: Node):
    if not isinstance(n, FunctionNode):
        return set()
    if n.op == '/':
        l_arg = n.args[0]
        r_arg = n.args[1]
        if isinstance(l_arg, FunctionNode) and l_arg.op == '*' and isinstance(r_arg, FunctionNode) and r_arg.op == '*' \
                and l_arg.args[1] == r_arg.args[1]:
            _n = FunctionNode(
                '*',
                [
                    FunctionNode('/', [l_arg.args[0], r_arg.args[0]]),
                    FunctionNode('/', [l_arg.args[1], r_arg.args[1]])
                ]
            )
            return {_n}
    return set()
# MARKDOWN


# This short-circuits the idea of removing constant integer factors by expanding out prime factors and then using
# equivalent_fraction_basic() to pull out those prime factors from the fraction.
def equivalent_fraction_constant_shortcircuit(n: Node):
    if not isinstance(n, FunctionNode):
        return set()
    if n.op == '/':
        l_arg = n.args[0]
        r_arg = n.args[1]
        if isinstance(l_arg, FunctionNode) and l_arg.op == '*' and isinstance(r_arg, FunctionNode) and r_arg.op == '*' \
                and isinstance(l_arg.args[1], ConstantNode) and isinstance(r_arg.args[1], ConstantNode):
            p1, p2 = l_arg.args[1].value, r_arg.args[1].value
            if p1 > 0:
                factors1 = factor_fastest(p1)
            elif p1 < 0:
                factors1 = factor_fastest(-p1)
                factors1 = {-f for f in factors1}
            else:
                return set()
            if p2 > 0:
                factors2 = factor_fastest(p2)
            elif p2 < 0:
                factors2 = factor_fastest(-p2)
                factors2 = {-f for f in factors2}
            else:
                return set()
            factor = max(factors1 & factors2)
            p1 = p1 // factor
            p2 = p2 // factor
            _n = FunctionNode(
                '/',
                [
                    FunctionNode('*', [l_arg.args[0], ConstantNode(p1)]),
                    FunctionNode('*', [r_arg.args[0], ConstantNode(p2)])
                ]
            )
            return {_n}
    return set()


def equivalent_fraction_exponent_shortcircuit(n: Node):
    def normalize_to_exponents(n1: Node, n2: Node):
        if isinstance(n1, FunctionNode) and n1.op == '^'\
                and isinstance(n2, FunctionNode) and n2.op == '^'\
                and n1.args[0] == n2.args[0]:
            return n1, n2
        elif isinstance(n1, FunctionNode) and n1.op == '^'\
                and n1.args[0] == n2:
            return n1, FunctionNode('^', [n2, ConstantNode(1)])
        elif isinstance(n2, FunctionNode) and n2.op == '^'\
                and n2.args[0] == n1:
            return FunctionNode('^', [n1, ConstantNode(1)]), n2
        else:
            return FunctionNode('^', [n1, ConstantNode(1)]), FunctionNode('^', [n2, ConstantNode(1)])

    def normalize_to_multiplication(n1: Node, n2: Node):
        if isinstance(n1, FunctionNode) and n1.op == '*' and isinstance(n2, FunctionNode) and n2.op == '*':
            return n1, n2
        elif isinstance(n1, FunctionNode) and n1.op == '*':
            return n1, FunctionNode('*', [ConstantNode(1), n2])
        elif isinstance(n2, FunctionNode) and n2.op == '*':
            return FunctionNode('*', [ConstantNode(1), n1]), n2
        else:
            return FunctionNode('*', [ConstantNode(1), n1]), FunctionNode('*', [ConstantNode(1), n2])

    if not isinstance(n, FunctionNode) or n.op != '/':
        return set()
    arg1, arg2 = n.args
    arg1, arg2 = normalize_to_multiplication(arg1, arg2)
    p1, p2 = arg1.args[1], arg2.args[1]
    p1, p2 = normalize_to_exponents(p1, p2)
    if p1.args[0] == p2.args[0] and isinstance(p1.args[1], ConstantNode) and isinstance(p2.args[1], ConstantNode):
        p_base = p1.args[0]
        p_min_exp = min(p1.args[1], p2.args[1])
        p_top_exp = p1.args[1] - p_min_exp
        p_bottom_exp = p2.args[1] - p_min_exp
        rhs_top = FunctionNode('^', [p_base, p_top_exp])
        rhs_bottom = FunctionNode('^', [p_base, p_bottom_exp])
        lhs_top = arg1.args[0]
        lhs_bottom = arg2.args[0]
        _n = FunctionNode(
            '*',
            [
                FunctionNode('/', [lhs_top, lhs_bottom]),
                FunctionNode('/', [rhs_top, rhs_bottom])
            ]
        )
        return {_n}
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
                print(f'    {to_string(n)} ⟶ {to_string(alt_n)}')
        print('```')
        print()
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    for r in equivalent_fraction(parse('(x*1)/(1*1)')):
        print(f'{to_string(r)}')
    for r in equivalent_fraction(parse('(1*1)/(x*1)')):
        print(f'{to_string(r)}')
    for r in equivalent_fraction(parse('(x*c)/(y*c)')):
        print(f'{to_string(r)}')
    for r in equivalent_fraction(parse('(1*c)/(1*c)')):
        print(f'{to_string(r)}')
    for r in equivalent_fraction(parse('(x*(t-1))/(y*(t-1))')):
        print(f'{to_string(r)}')

    for r in equivalent_fraction_constant_shortcircuit(parse('(x*5)/(y*10)')):
        print(f'{to_string(r)}')

    for r in equivalent_fraction_exponent_shortcircuit(parse('(5*x^2)/(x^3)')):
        print(f'{to_string(r)}')
    for r in equivalent_fraction_exponent_shortcircuit(parse('(z*x)/(y*x^5)')):
        print(f'{to_string(r)}')
    for r in equivalent_fraction_exponent_shortcircuit(parse('(z*x^5)/(y*x)')):
        print(f'{to_string(r)}')