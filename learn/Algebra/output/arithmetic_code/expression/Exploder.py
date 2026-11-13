from expression.Node import Node, FunctionNode
from expression.Utils import extract_numeric_constants
from expression.parser.Parser import parse
from expression.parser.Printer import to_string
from expression.properties import ExponentProductProperty, \
    ExponentProductToPowerProperty, NegativeExponentDefinition, ZeroExponentDefinition, EquivalentFractionProperty, \
    ExponentQuotientProperty, ExponentQuotientToPowerProperty, ExponentPowerProperty, \
    DistributiveProperty, OneExponentDefinition, RatioAdditionProperties, \
    RatioSubtractionProperties, RatioMultiplicationProperties, RatioDivisionProperties, ArithmeticConversions


class ExplosionCache:
    __slots__ = ['contract_cache', 'recursive_contract', 'recursive_contract_top', 'shuffle_cache', 'explode_cache']

    def __init__(self):
        self.contract_cache = {}
        self.recursive_contract = {}
        self.recursive_contract_top = {}
        self.shuffle_cache = {}
        self.explode_cache = {}


def contract(n: Node, cache: ExplosionCache):
    if n in cache.contract_cache:
        return cache.contract_cache[n]
    options = set()
    operations = [
        ArithmeticConversions.sub_to_add,
        ArithmeticConversions.add_to_mul,
        ArithmeticConversions.mul_to_exp,
        RatioAdditionProperties.evaluate,
        RatioAdditionProperties.commutative,
        RatioAdditionProperties.associative,
        RatioAdditionProperties.identity,
        RatioAdditionProperties.inverse,
        RatioMultiplicationProperties.evaluate,
        RatioMultiplicationProperties.commutative,
        RatioMultiplicationProperties.associative,
        RatioMultiplicationProperties.identity,
        RatioMultiplicationProperties.inverse,
        RatioSubtractionProperties.evaluate,
        RatioSubtractionProperties.identity,
        RatioSubtractionProperties.inverse,
        RatioDivisionProperties.evaluate,
        RatioDivisionProperties.identity,
        RatioDivisionProperties.inverse,
        OneExponentDefinition.from_one_exponent,
        ZeroExponentDefinition.zero_exponent,
        RatioMultiplicationProperties.zero,
        RatioDivisionProperties.zero
    ]
    for op in operations:
        op_name = op.__name__
        op_results = op(n)
        options |= {(op_name, r) for r in op_results}
    if isinstance(n, FunctionNode):
        for arg_idx, arg in enumerate(n.args):
            for rule, arg_tweaked in contract(arg, cache):
                new_fn_args = list(n.args)
                new_fn_args[arg_idx] = arg_tweaked
                fn = FunctionNode(n.op, new_fn_args)
                options.add((rule, fn))
    cache.contract_cache[n] = options
    return options


def recursive_contract(n: Node, cache: ExplosionCache):
    orig_n = n
    if orig_n in cache.recursive_contract:
        return cache.recursive_contract[orig_n]
    processed = {}
    options = {orig_n: []}
    while options:
        n = next(iter(options))
        n_rules = options[n]
        new_options = contract(n, cache)
        for _n_rule, _n in new_options:
            _n_rules = n_rules + [(_n_rule, _n)]
            if _n in processed:
                _n_rules_existing = processed[_n]
                if len(_n_rules) < len(_n_rules_existing):
                    processed[_n] = _n_rules
            elif _n in options:
                _n_rules_existing = options[_n]
                if len(_n_rules) < len(_n_rules_existing):
                    options[_n] = _n_rules
            else:
                options[_n] = _n_rules
        n_rules = options[n]
        processed[n] = n_rules
        options.pop(n)
    cache.recursive_contract[orig_n] = processed
    return processed


def recursive_contract_top(n: Node, cache: ExplosionCache):
    if n in cache.recursive_contract_top:
        return cache.recursive_contract_top[n]
    processed = recursive_contract(n, cache)
    smallest_op_count = min(n.op_count for n in processed)
    processed = {n: n_rules for n, n_rules in processed.items() if n.op_count == smallest_op_count}

    def max_numeric_const(n: Node) -> int | None:
        return max((c.value for c in extract_numeric_constants(n)), default=0)

    def min_numeric_const(n: Node) -> int | None:
        return min((c.value for c in extract_numeric_constants(n)), default=0)

    min_consts = {n: min_numeric_const(n) for n in processed}
    max_consts = {n: max_numeric_const(n) for n in processed}
    max_const_magnitudes = {n: max(abs(min_consts[n]), abs(max_consts[n])) for n in processed}
    smallest_max_const_magnitude = min(max_const_magnitudes[n] for n in processed)
    processed = {n: n_rules for n, n_rules in processed.items() if max_const_magnitudes[n] == smallest_max_const_magnitude}
    n, n_rules = next(iter(processed.items()))
    cache.recursive_contract_top[n] = n, n_rules
    return n, n_rules


def shuffle(n: Node, cache: ExplosionCache):
    if n in cache.shuffle_cache:
        return cache.shuffle_cache[n]
    if not isinstance(n, FunctionNode):
        return set()
    options = set()
    operations = [
        ArithmeticConversions.sub_to_add,
        ArithmeticConversions.add_to_mul,
        ArithmeticConversions.mul_to_exp,
        RatioAdditionProperties.commutative,
        RatioAdditionProperties.associative,
        RatioAdditionProperties.combine,
        RatioAdditionProperties.uncombine,
        RatioMultiplicationProperties.commutative,
        RatioMultiplicationProperties.associative,
        RatioMultiplicationProperties.combine,
        RatioMultiplicationProperties.uncombine,
        RatioSubtractionProperties.combine,
        RatioSubtractionProperties.uncombine,
        RatioDivisionProperties.combine,
        RatioDivisionProperties.uncombine,
        DistributiveProperty.distributive,
        DistributiveProperty.undistributive,
        EquivalentFractionProperty.equivalent_fraction,
        ExponentPowerProperty.exponent_power,
        ExponentPowerProperty.unexponent_power,
        ExponentProductProperty.exponent_product,
        ExponentProductProperty.unexponent_product,
        ExponentProductToPowerProperty.exponent_product_to_power,
        ExponentProductToPowerProperty.unexponent_product_to_power,
        ExponentQuotientProperty.exponent_quotient,
        ExponentQuotientProperty.unexponent_quotient,
        ExponentQuotientToPowerProperty.exponent_quotient_to_power,
        ExponentQuotientToPowerProperty.unexponent_quotient_to_power,
        NegativeExponentDefinition.from_negative_exponent,
        NegativeExponentDefinition.to_negative_exponent,
    ]
    for op in operations:
        op_name = op.__name__
        op_results = op(n)
        for _n in op_results:
            _n, _n_rules = recursive_contract_top(_n, cache)
            # _n_rules = ((op_name, _n), ) + tuple(_n_rules)
            # options.add((_n_rules, _n))
            options.add((op_name, _n))
    for n_arg_idx, n_arg in enumerate(n.args):
        for _n_arg_tweaked_rule, _n_arg_tweaked in shuffle(n_arg, cache):
            _n_args = list(n.args)
            _n_args[n_arg_idx] = _n_arg_tweaked
            _n = FunctionNode(n.op, _n_args)
            options.add((_n_arg_tweaked_rule, _n))
    cache.shuffle_cache[n] = options
    return options


def explode(n: Node, cache: ExplosionCache):
    if n in cache.explode_cache:
        return cache.explode_cache[n]
    processed = {}
    n_rules = (('start', n), )
    n_contracted, n_contracted_rules = recursive_contract_top(n, cache)
    options = {n_contracted: n_rules + tuple(n_contracted_rules)}
    while options:
        n = next(iter(options))
        n_rules = options[n]
        new_options = shuffle(n, cache)
        for _n_rule, _n in new_options:
            # new_tree_contracted, new_tree_contracted_rules = recursive_contract_top(_n, cache)
            # _n_rules = n_rules + [(_n_rules, _n)] + new_tree_contracted_rules
            # _n = new_tree_contracted
            _n_rules = n_rules + ((_n_rule, _n), )
            if _n in processed:
                _n_rules_existing = processed[_n]
                if len(_n_rules) < len(_n_rules_existing):
                    processed[_n] = _n_rules
            elif _n in options:
                _n_rules_existing = options[_n]
                if len(_n_rules) < len(_n_rules_existing):
                    options[_n] = _n_rules
            else:
                options[_n] = _n_rules
        n_rules = options[n]
        processed[n] = n_rules
        options.pop(n)
        # print(f'{to_string(n)}   >>> {", ".join(f"{c_op}: {to_string(c_tree)}" for c_op, c_tree in n_rules)}')
    cache.explode_cache[n] = processed
    return processed


def simplify(n: Node, cache: ExplosionCache | None = None):
    if cache is None:
        cache = ExplosionCache()
    options = explode(n, cache)
    simplified = min(options.keys(), key=lambda _n: _n.op_count)
    return simplified, options[simplified]


if __name__ == '__main__':
    # tree = parse('2 + -2 ^ x + 3 * 4 / (2*x)')
    # tree = parse('-1*(-x-y)')
    # tree = parse('(x + (x*-2)) + (x-4)')
    # tree = parse('x + (x+1) + x')
    tree = parse('x-x')
    # tree = parse('-1*(-1*x)')
    # tree = parse('-1*(-1*x+-1*y)')
    # tree = parse('8 / log(2, 32) + (8^x)^x')
    # tree = parse('(5 * 5) * (5 * 5)')
    # tree = parse('5')
    # tree = parse('a+b+c/d')
    # tree = parse('(6+2)/4')
    # tree = parse('0/x')
    # tree = parse('(a/b)/c')
    # tree = parse('x+y+z')
    # tree = parse('4*x-2')
    # tree = parse('x*x-2')
    import cProfile
    pr = cProfile.Profile()
    pr.enable()
    cache = ExplosionCache()
    variations = explode(tree, cache)
    pr.disable()
    pr.print_stats(sort='time')
    for _tree, _tree_path in variations.items():
        # print(f'{_tree} {_tree_path}')
        print(f'{to_string(_tree)}')
        for rule, _tree in _tree_path:
            print(f'>> {rule}: {to_string(_tree)}')
    print('SIMPLIFIED')
    print('----------')
    tree, tree_chain = simplify(tree, cache)
    print(f'{to_string(tree)}')
    for rule, tree in tree_chain:
        print(f'>> {rule}: {to_string(tree)}')
