from expression.parser.Parser import FunctionNode, parse, ConstantNode, Node
from expression.parser.Printer import to_string


PRIOR_EQUIV_FORMS = 'prior_equiv_forms'


def div_to_mul_raw(fn: FunctionNode):
    lhs = fn.args[0]
    rhs = fn.args[1]
    rhs_inverted = FunctionNode('/', [ConstantNode(1), rhs])
    return FunctionNode('*', [lhs, rhs_inverted])


def div_to_mul(fn: Node):
    if not isinstance(fn, FunctionNode) or fn.op != '/':
        return set()
    prior_fns = fn.annotations.get(PRIOR_EQUIV_FORMS, [])
    for prior_fn in prior_fns:
        prior_fn_adjusted = div_to_mul_raw(prior_fn)
        if prior_fn_adjusted in prior_fns or prior_fn_adjusted == fn:
            return set()
    new_fn = div_to_mul_raw(fn)
    new_fn.annotations[PRIOR_EQUIV_FORMS] = prior_fns[:] + [fn]
    return {new_fn}


def mul_to_div_raw(fn: FunctionNode):
    lhs = fn.args[0]
    rhs = fn.args[1]
    rhs_negated = FunctionNode('/', [ConstantNode(1), rhs])
    return FunctionNode('/', [lhs, rhs_negated])


def mul_to_div(fn: Node):
    if not isinstance(fn, FunctionNode) or fn.op != '*':
        return set()
    prior_fns = fn.annotations.get(PRIOR_EQUIV_FORMS, [])
    for prior_fn in prior_fns:
        prior_fn_adjusted = mul_to_div_raw(prior_fn)
        if prior_fn_adjusted in prior_fns or prior_fn_adjusted == fn:
            return set()
    new_fn = mul_to_div_raw(fn)
    new_fn.annotations[PRIOR_EQUIV_FORMS] = prior_fns[:] + [fn]
    return {new_fn}


if __name__ == '__main__':
    for r in mul_to_div(parse('5*4')):
        print(f'{to_string(r)}')
    for r in div_to_mul(parse('5/2')):
        print(f'{to_string(r)}')
