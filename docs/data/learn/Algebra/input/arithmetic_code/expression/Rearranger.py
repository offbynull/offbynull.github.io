import math
from fractions import Fraction

from expression.Utils import count_functions
from expression.parser.Parser import FunctionNode, parse, VariableNode, ConstantNode, Node
from expression.parser.Printer import to_string
from expression.properties import InverseProperty, IdentityProperty, ExponentProductProperty, \
    ExponentProductToPowerProperty, NegativeExponentDefinition, ZeroExponentDefinition, EquivalentFractionProperty, \
    ExponentQuotientProperty, AssociativeProperty, ExponentQuotientToPowerProperty, ExponentPowerProperty, \
    DistributiveProperty, CommutativeProperty, AdditionSubtractionConversion, OneExponentDefinition


def evaluate(x: FunctionNode):
    if x.op == '+' and isinstance(x.args[0], ConstantNode) and isinstance(x.args[1], ConstantNode):
        return ConstantNode(x.args[0].value + x.args[1].value)
    elif x.op == '-' and isinstance(x.args[0], ConstantNode) and isinstance(x.args[1], ConstantNode):
        return ConstantNode(x.args[0].value - x.args[1].value)
    elif x.op == '*' and isinstance(x.args[0], ConstantNode) and isinstance(x.args[1], ConstantNode):
        return ConstantNode(x.args[0].value * x.args[1].value)
    elif x.op == '/' and isinstance(x.args[0], ConstantNode) and isinstance(x.args[1], ConstantNode):
        return ConstantNode(x.args[0].value / x.args[1].value)
    elif x.op == '^' and isinstance(x.args[0], ConstantNode) and isinstance(x.args[1], ConstantNode):
        return ConstantNode(x.args[0].value ** x.args[1].value)
    elif x.op == 'log' and isinstance(x.args[0], ConstantNode) and isinstance(x.args[1], ConstantNode):
        return ConstantNode(math.log(x.args[1].value, x.args[0].value))
    # elif x.op == 'root' and isinstance(x.args[0], Fraction) and isinstance(x.args[1], Fraction):
    #     return {x.args[0]**(1/x.args[1])}
    return None


def drill_evaluate(x: Node):
    if not isinstance(x, FunctionNode):
        return x
    found = evaluate(x)
    if found is not None:
        return found
    x = FunctionNode(x.op, x.args[:], x.annotations)
    for arg_idx, arg in enumerate(x.args):
        x.args[arg_idx] = drill_evaluate(arg)
    return x


def drill(x: Node):
    if not isinstance(x, FunctionNode):
        return {x}
    options = {x}
    options |= AdditionSubtractionConversion.sub_to_add(x)
    options |= AdditionSubtractionConversion.add_to_sub(x)
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
    options |= OneExponentDefinition.one_exponent(x)
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
                    new_fn = FunctionNode(new_fn.op, new_fn_args, new_fn.annotations)
                    inner_options.add(new_fn)
    return options | inner_options


def rearrange(x: Node):
    x = drill_evaluate(x)
    processed = {}
    options = {x: [x]}
    while options:
        tree = next(iter(options))
        tree_chain = options[tree]
        new_options = drill(tree)
        for t in new_options:
            t = drill_evaluate(t)
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
        # print(f'{to_string(tree)}: {tree_chain} {tree.annotations}')
    return processed


def simplify(x: Node):
    variations = rearrange(x)
    simplifed = min(variations.keys(), key=lambda x: count_functions(x))
    return simplifed, variations[simplifed]


if __name__ == '__main__':
    tree = parse('5 + -4 ^ x + 3 * 8 / log(2, 32)')
    # tree = parse('4*x-2')
    # tree = parse('x*x-2')
    variations = rearrange(tree)
    for _tree, _tree_path in variations.items():
        print(f'{_tree}: {_tree_path}')
    print(f'{simplify(tree)}')
