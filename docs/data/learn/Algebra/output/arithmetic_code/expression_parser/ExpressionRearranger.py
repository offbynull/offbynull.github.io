from fractions import Fraction

from Factor import factor_fastest
from expression_parser.Parser import FunctionNode, parse_expression
from expression_parser.StringStream import StringStream


def rearrange(x: FunctionNode | Fraction | str):
    variations = {x}
    # Explode to factors (if number)
    exploded_variations = set()
    for v in variations:
        if isinstance(v, Fraction) and v.denominator == 1:
            exploded_variations |= rearrange_explode_factors(v)
    variations |= exploded_variations
    # Apply rearrangement on each argument of each variation (if the variation is a function)
    rearranged_arg_variations = set()
    for v in variations:
        if not isinstance(v, FunctionNode):
            continue
        for i, arg in enumerate(v.args):
            for arg_variation in rearrange(arg):
                _fn = FunctionNode(v.op, v.args.copy())
                _fn.args[i] = arg_variation
                rearranged_arg_variations.add(_fn)
    variations |= rearranged_arg_variations
    # Apply algebra rules (if function)
    rearranged_arg_variations = set()
    for v in variations:
        if isinstance(v, FunctionNode):
            # Commutative / associative rules
            if v.op in '+*':
                rearranged_arg_variations |= rearrange_commutative(v)
                rearranged_arg_variations |= rearrange_associative(v)
            # Compute result if operands are numbers
            rearranged_arg_variations |= rearrange_compute(v)
    variations |= rearranged_arg_variations
    return variations

def rearrange_explode_factors(f: Fraction):
    assert isinstance(f, Fraction) and f.denominator == 1
    variations = {f}
    for factor1 in factor_fastest(f.numerator):
        factor2 = f // factor1
        if factor1 == 1 or factor2 == 1:
            continue
        inner_fn = FunctionNode('*', [Fraction(factor1), Fraction(factor2)])
        variations.add(inner_fn)
    return variations

def rearrange_compute(fn: FunctionNode):
    variations = {fn}
    if fn.op == '+' and isinstance(fn.args[0], Fraction) and isinstance(fn.args[1], Fraction):
        variations.add(fn.args[0] + fn.args[1])
    elif fn.op == '*' and isinstance(fn.args[0], Fraction) and isinstance(fn.args[1], Fraction):
        variations.add(fn.args[0] * fn.args[1])
    elif fn.op == '-' and isinstance(fn.args[0], Fraction) and isinstance(fn.args[1], Fraction):
        variations.add(fn.args[0] - fn.args[1])
    elif fn.op == '/' and isinstance(fn.args[0], Fraction) and isinstance(fn.args[1], Fraction):
        variations.add(fn.args[0] / fn.args[1])
    elif fn.op == '^' and isinstance(fn.args[0], Fraction) and isinstance(fn.args[1], Fraction):
        variations.add(fn.args[0] ** fn.args[1])
    return variations

def rearrange_commutative(fn: FunctionNode):
    assert fn.op in '+*'
    variations = {fn}
    _fn = FunctionNode(
        fn.op,
        fn.args[::-1]
    )
    variations.add(_fn)
    return variations

def rearrange_associative(fn: FunctionNode):
    assert fn.op in '+*'
    variations = {fn}
    l_arg = fn.args[0]
    r_arg = fn.args[1]
    if isinstance(fn.args[0], FunctionNode) and fn.args[0].op == fn.op:
        _fn = FunctionNode(
            fn.op,
            [
                l_arg.args[0],
                FunctionNode(fn.op, [l_arg.args[1], r_arg])
            ]
        )
        variations.add(_fn)
    if isinstance(fn.args[1], FunctionNode) and fn.args[1].op == fn.op:
        _fn = FunctionNode(
            fn.op,
            [
                FunctionNode(fn.op, [l_arg, r_arg.args[0]]),
                r_arg.args[1]
            ]
        )
        variations.add(_fn)
    return variations


if __name__ == '__main__':
    tree = parse_expression(StringStream('5 + 4 ^ x + 3 * 8 / log(2, 32)'))
    # tree = parse_expression(StringStream('(1*2)*3'))
    variations = rearrange(tree)
    for t in variations:
        print(f'{t}')
