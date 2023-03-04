import inspect
import sys
from pathlib import Path
from sys import stdin

import yaml

from Factor import factor_tree
from expression.Node import Node, ConstantNode, FunctionNode, VariableNode
from expression.parser.Parser import parse
from expression.parser.Printer import to_string


# MARKDOWN_PRIME_FACTORS
def prime_factors(n: Node):
    if not isinstance(n, ConstantNode):
        return set()
    negative = n < 0
    if negative:
        n = -n
    if n in {0, 1, -1}:
        return set()
    factors = factor_tree(n.value.numerator).get_prime_factors()
    last = ConstantNode(factors.pop())
    while factors:
        new = ConstantNode(factors.pop())
        last = FunctionNode('*', [last, new])
    if negative:
        last = FunctionNode('*', [ConstantNode(-1), last])
    return {last}
# MARKDOWN_PRIME_FACTORS


# MARKDOWN_ADD_SUB
def sub_to_add(n: FunctionNode):
    if isinstance(n, FunctionNode) and n.op == '-':
        lhs = n.args[0]
        rhs = n.args[1]
        rhs_negated = FunctionNode('*', [ConstantNode(-1), rhs])
        _n = FunctionNode('+', [lhs, rhs_negated])
        return {_n}
    return set()


def add_to_sub(n: FunctionNode):
    if isinstance(n, FunctionNode) and n.op == '+':
        lhs = n.args[0]
        rhs = n.args[1]
        rhs_negated = FunctionNode('*', [ConstantNode(-1), rhs])
        _n = FunctionNode('-', [lhs, rhs_negated])
        return {_n}
    return set()
# MARKDOWN_ADD_SUB


# MARKDOWN_ADD_MUL
def add_to_mul(n: Node):
    if isinstance(n, FunctionNode) and n.op == '+':
        lhs, rhs = n.args
        lhs_const, lhs_factor = _split_out_multiplication_constant(lhs)
        rhs_const, rhs_factor = _split_out_multiplication_constant(rhs)
        if lhs_const is None or lhs_factor is None or rhs_const is None or rhs_factor is None:
            return set()
        if lhs_factor != rhs_factor:
            return set()
        _n = FunctionNode('*', [lhs_const + rhs_const, lhs_factor])
        return {_n}
    return set()


def mul_to_add(n: Node):
    if isinstance(n, FunctionNode) and n.op == '*':
        const, factor = _split_out_multiplication_constant(n)
        if factor is None or const is None:
            return set()
        if const > 0:
            _n = factor
            while const > 1:
                _n = FunctionNode('+', [factor, _n])
                const = const - 1
            return {_n}
    return set()


def _split_out_multiplication_constant(a: Node):
    if isinstance(a, ConstantNode) or isinstance(a, VariableNode):
        return ConstantNode(1), a
    elif isinstance(a, FunctionNode) and a.op == '*' and isinstance(a.args[0], ConstantNode):
        a_lhs, a_rhs = a.args
        return a_lhs, a_rhs
    return None, None
# MARKDOWN_ADD_MUL


# MARKDOWN_MUL_EXP
def mul_to_exp(n: FunctionNode):
    if isinstance(n, FunctionNode) and n.op == '*':
        lhs, rhs = n.args
        lhs_base, lhs_const = _split_out_exponent_constant(lhs)
        rhs_base, rhs_const = _split_out_exponent_constant(rhs)
        if lhs_const is None or lhs_base is None or rhs_const is None or rhs_base is None:
            return set()
        if lhs_base != rhs_base:
            return set()
        _n = FunctionNode('^', [lhs_base, lhs_const + rhs_const])
        return {_n}
    return set()


def exp_to_mul(n: FunctionNode):
    if isinstance(n, FunctionNode) and n.op == '^':
        base, exp = _split_out_exponent_constant(n)
        if base is None or exp is None:
            return set()
        if exp > 0:
            _n = base
            while exp > 1:
                _n = FunctionNode('*', [base, _n])
                exp = exp - 1
            return {_n}
    return set()


def _split_out_exponent_constant(a: Node):
    if isinstance(a, ConstantNode) or isinstance(a, VariableNode):
        return a, ConstantNode(1)
    elif isinstance(a, FunctionNode) and a.op == '^' and isinstance(a.args[1], ConstantNode):
        a_lhs, a_rhs = a.args
        return a_lhs, a_rhs
    return None, None
# MARKDOWN_MUL_EXP


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
    main()
