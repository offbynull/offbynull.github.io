from fractions import Fraction

from expression.parser.Parser import FunctionNode, parse, ConstantNode, Node
from expression.parser.Printer import to_string


PRIOR_EQUIV_FORMS = 'prior_equiv_forms'


def one_exponent(fn: Node):
    if isinstance(fn, FunctionNode) and fn.op == '^':
        l_arg = fn.args[0]
        r_arg = fn.args[1]
        if r_arg == 1:
            return {l_arg}
    return set()


def unone_exponent_raw(fn: Node):
    return FunctionNode('^', [fn, ConstantNode(1)])


def unone_exponent(fn: Node):
    prior_fns = fn.annotations.get(PRIOR_EQUIV_FORMS, [])
    for prior_fn in prior_fns:
        prior_fn_adjusted = unone_exponent_raw(prior_fn)
        if prior_fn_adjusted in prior_fns or prior_fn_adjusted == fn:
            return set()
    new_fn = unone_exponent_raw(fn)
    new_fn.annotations[PRIOR_EQUIV_FORMS] = prior_fns[:] + [fn]
    return {new_fn}


if __name__ == '__main__':
    for r in one_exponent(parse('x^1')):
        print(f'{to_string(r)}')
    for r in unone_exponent(parse('x')):
        print(f'{to_string(r)}')
        for r1 in unone_exponent(r):
            print(f'>>{to_string(r)}')