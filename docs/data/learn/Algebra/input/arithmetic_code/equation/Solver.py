from equation.Equality import Equality
from equation.properties.AdditionProperty import addition
from equation.properties.DivisionProperty import division
from equation.properties.MultiplicationProperty import multiplication
from equation.properties.SubtractionProperty import subtraction
from expression.Exploder import ExplosionCache, simplify
from expression.Utils import swap_variables, extract_variables
from expression.parser.Parser import VariableNode, parse, Node, ConstantNode, FunctionNode


def isolate(eq: Equality, variable: VariableNode):
    cache = ExplosionCache()
    processed = set()
    options = {eq}
    while options:
        _eq = options.pop()
        # print(f'{_eq}')
        if _eq.lhs == variable:
            return _eq
        elif _eq.rhs == variable:
            return _eq
        new_options = set()
        new_options |= addition(_eq, cache)
        new_options |= division(_eq, cache)
        new_options |= multiplication(_eq, cache)
        new_options |= subtraction(_eq, cache)
        processed.add(eq)
        for _eq in new_options:
            if _eq not in options and _eq not in processed:
                options.add(_eq)
    raise ValueError('Unable to isolate')


def is_solution(
        eq: Equality,
        var_replacements: dict[VariableNode, Node]
):
    lhs = swap_variables(eq.lhs, var_replacements)
    lhs, _ = simplify(lhs)
    rhs = swap_variables(eq.rhs, var_replacements)
    rhs, _ = simplify(rhs)
    if not isinstance(lhs, ConstantNode) or not isinstance(rhs, ConstantNode):
        raise ValueError(f'Missing variable replacements = {extract_variables(lhs) | extract_variables(rhs)}')
    if isinstance(lhs, ConstantNode) and isinstance(rhs, ConstantNode) and lhs == rhs:
        return True
    elif isinstance(lhs, FunctionNode) and lhs.op == '/' \
            and isinstance(rhs, FunctionNode) and rhs.op == '/'\
            and isinstance(lhs.args[0], ConstantNode) and isinstance(lhs.args[1], ConstantNode)\
            and isinstance(rhs.args[0], ConstantNode) and isinstance(rhs.args[1], ConstantNode)\
            and lhs.args == rhs.args:
        return True
    return False


if __name__ == '__main__':
    # eq = Equality(parse('2*x'), parse('4'))
    # eq_isolated = isolate(eq, VariableNode('x'))
    # print(f'{eq_isolated}')
    eq = Equality(parse('4*x-2'), parse('2*x+1'))
    solution = is_solution(eq, {VariableNode('x'): FunctionNode('/', [ConstantNode(3), ConstantNode(2)])})
    print(f'{solution}')
