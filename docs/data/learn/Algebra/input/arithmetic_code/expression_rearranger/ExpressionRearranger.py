import math
from fractions import Fraction

from expression_parser.Parser import FunctionNode, parse, VariableNode
from expression_rearranger import AssociativeProperty, CommutativeProperty, DistributiveProperty, \
    EquivalentFractionProperty, ExponentPowerProperty, ExponentProductProperty, ExponentQuotientProperty, \
    ExponentProductToPowerProperty, ExponentQuotientToPowerProperty, IdentityProperty, InverseProperty, \
    NegativeExponentDefinition, ZeroExponentDefinition


def evaluate(x: FunctionNode | VariableNode | Fraction):
    if not isinstance(x, FunctionNode):
        return {x}
    if x.op == '+' and isinstance(x.args[0], Fraction) and isinstance(x.args[1], Fraction):
        return {Fraction(x.args[0] + x.args[1])}
    elif x.op == '-' and isinstance(x.args[0], Fraction) and isinstance(x.args[1], Fraction):
        return {Fraction(x.args[0] - x.args[1])}
    elif x.op == '*' and isinstance(x.args[0], Fraction) and isinstance(x.args[1], Fraction):
        return {Fraction(x.args[0] * x.args[1])}
    elif x.op == '/' and isinstance(x.args[0], Fraction) and isinstance(x.args[1], Fraction):
        return {Fraction(x.args[0] / x.args[1])}
    elif x.op == '^' and isinstance(x.args[0], Fraction) and isinstance(x.args[1], Fraction):
        return {Fraction(x.args[0] ** x.args[1])}
    elif x.op == 'log' and isinstance(x.args[0], Fraction) and isinstance(x.args[1], Fraction):
        return {Fraction(math.log(x.args[1], x.args[0]))}
    # elif x.op == 'root' and isinstance(x.args[0], Fraction) and isinstance(x.args[1], Fraction):
    #     return {x.args[0]**(1/x.args[1])}
    return {x}


def drill(x: FunctionNode | VariableNode | Fraction):
    if not isinstance(x, FunctionNode):
        return {x}
    options = {x}
    options |= CommutativeProperty.commutative(x)
    options |= AssociativeProperty.associative(x)
    options |= DistributiveProperty.distributive(x)
    options |= DistributiveProperty.undistributive(x)
    options |= EquivalentFractionProperty.equivalent_fraction(x)
    options |= EquivalentFractionProperty.unequivalent_fraction(x)
    options |= ExponentPowerProperty.exponent_product(x)
    options |= ExponentPowerProperty.unexponent_product(x)
    options |= ExponentProductProperty.exponent_product(x)
    options |= ExponentProductProperty.unexponent_product(x)
    options |= ExponentProductToPowerProperty.exponent_product_to_power(x)
    options |= ExponentProductToPowerProperty.unexponent_product_to_power(x)
    options |= ExponentQuotientProperty.exponent_quotient(x)
    options |= ExponentQuotientProperty.unexponent_quotient(x)
    options |= ExponentQuotientToPowerProperty.exponent_quotient_to_power(x)
    options |= ExponentQuotientToPowerProperty.unexponent_product_to_power(x)
    options |= IdentityProperty.identity(x)
    options |= InverseProperty.inverse(x)
    options |= NegativeExponentDefinition.negative_exponent(x)
    options |= NegativeExponentDefinition.unnegative_exponent(x)
    options |= ZeroExponentDefinition.zero_exponent(x)
    options |= evaluate(x)
    inner_options = set()
    for new_fn in options:
        if not isinstance(new_fn, FunctionNode):
            inner_options.add(new_fn)
        else:
            for arg_idx, arg in enumerate(new_fn.args):
                tweaked = drill(arg)
                for t in tweaked:
                    new_fn_args = new_fn.args[:]
                    new_fn_args[arg_idx] = t
                    new_fn = FunctionNode(new_fn.op, new_fn_args)
                    inner_options.add(new_fn)
    return options | inner_options


def rearrange(x: FunctionNode | VariableNode | Fraction):
    processed = {}
    options = {x: [x]}
    while options:
        tree = next(iter(options))
        tree_chain = options[tree]
        new_options = drill(tree)
        for t in new_options:
            new_chain = tree_chain + [t]
            if t in processed:
                old_chain = processed[t]
                if len(new_chain) < len(old_chain):
                    processed[t] = new_chain
            elif t in options:
                old_chain = options[t]
                if len(new_chain) < len(old_chain):
                    options[t] = new_chain
            else:
                options[t] = new_chain
        tree_chain = options[tree]
        processed[tree] = tree_chain
        options.pop(tree)
    return processed


if __name__ == '__main__':
    tree = parse('5 + -4 ^ x + 3 * 8 / log(2, 32)')
    variations = rearrange(tree)
    for tree, tree_path in variations.items():
        print(f'{tree}: {tree_path}')
