from expression.parser.Parser import FunctionNode, parse, ConstantNode, Node
from expression.parser.Printer import to_string


PRIOR_EQUIV_FORMS = 'prior_equiv_forms'


def sub_to_add_raw(fn: FunctionNode):
    lhs = fn.args[0]
    rhs = fn.args[1]
    rhs_negated = FunctionNode('*', [ConstantNode(-1), rhs])
    return FunctionNode('+', [lhs, rhs_negated])


def sub_to_add(fn: Node):
    if not isinstance(fn, FunctionNode) or fn.op != '-':
        return set()
    prior_fns = fn.annotations.get(PRIOR_EQUIV_FORMS, [])
    for prior_fn in prior_fns:
        prior_fn_adjusted = sub_to_add_raw(prior_fn)
        if prior_fn_adjusted in prior_fns or prior_fn_adjusted == fn:
            return set()
    new_fn = sub_to_add_raw(fn)
    new_fn.annotations[PRIOR_EQUIV_FORMS] = prior_fns[:] + [fn]
    return {new_fn}


def add_to_sub_raw(fn: FunctionNode):
    lhs = fn.args[0]
    rhs = fn.args[1]
    rhs_negated = FunctionNode('*', [ConstantNode(-1), rhs])
    return FunctionNode('-', [lhs, rhs_negated])


def add_to_sub(fn: Node):
    if not isinstance(fn, FunctionNode) or fn.op != '+':
        return set()
    prior_fns = fn.annotations.get(PRIOR_EQUIV_FORMS, [])
    for prior_fn in prior_fns:
        prior_fn_adjusted = add_to_sub_raw(prior_fn)
        if prior_fn_adjusted in prior_fns or prior_fn_adjusted == fn:
            return set()
    new_fn = add_to_sub_raw(fn)
    new_fn.annotations[PRIOR_EQUIV_FORMS] = prior_fns[:] + [fn]
    return {new_fn}


if __name__ == '__main__':
    r = parse('2-x')
    print(f'{to_string(r)}')
    for r1 in sub_to_add(r):
        print(f'>>{to_string(r1)}')
        for r2 in add_to_sub(r1):
            print(f'>>>>{to_string(r2)}')
            for r3 in sub_to_add(r2):
                print(f'>>>>>>{to_string(r3)}')
                for r4 in add_to_sub(r3):
                    print(f'>>>>>>>>{to_string(r4)}')
    # for r in add_to_sub(parse('(4*x)+(-1*y)')):
    #     print(f'{to_string(r)}')
