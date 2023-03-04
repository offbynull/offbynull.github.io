from expression.Exploder import simplify
from expression.Utils import swap_variables, extract_variables
from expression.parser.Parser import VariableNode, parse, Node, ConstantNode, FunctionNode


def is_solution(
        lhs: Node,
        rhs: Node,
        var_replacements: dict[VariableNode, Node]
):
    lhs = swap_variables(lhs, var_replacements)
    lhs, _ = simplify(lhs)
    rhs = swap_variables(rhs, var_replacements)
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
    tree_lhs = parse('4*x-2')
    tree_rhs = parse('2*x+1')
    solved = is_solution(tree_lhs, tree_rhs, {VariableNode('x'): FunctionNode('/', [ConstantNode(3), ConstantNode(2)])})
    print(f'{solved}')
