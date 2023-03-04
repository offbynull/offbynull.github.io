from expression.Node import Node, FunctionNode, ConstantNode
from expression.parser.Parser import parse
from relation.Relation import Relation
from relation.parser.Printer import to_string


def find_domain(n: Node) -> set[Relation]:
    ret = set()
    if isinstance(n, FunctionNode):
        for a in n.args:
            ret |= find_domain(a)
        if n.op == '/':
            ret |= {
                Relation('>', n.args[1], ConstantNode(0)),
                Relation('<', n.args[1], ConstantNode(0))
            }
        elif n.op == 'log':
            ret |= {
                Relation('>', n.args[1], ConstantNode(0)),
                Relation('<', n.args[1], ConstantNode(0))
            }
    return ret


if __name__ == '__main__':
    n = parse('x/(x/(1/x))')
    for r in find_domain(n):
        print(f'{to_string(r)}')
