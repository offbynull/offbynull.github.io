from typing import Union

from breakpoint_graph.SyntenyNode import SyntenyNode
from breakpoint_graph.TerminalNode import TerminalNode


class ColoredEdge:
    def __init__(
            self,
            n1: Union[SyntenyNode, TerminalNode],
            n2: Union[SyntenyNode, TerminalNode]
    ):
        assert isinstance(n1, SyntenyNode) or isinstance(n2, SyntenyNode), 'Both ends cant\'t be at terminal node'
        assert n1 != n2, 'Both ends can\'t be equal'
        # sort such that nodes are always placed in the same order
        if isinstance(n1, SyntenyNode) and isinstance(n2, SyntenyNode):  # both synteny nodes? n1 should be smaller
            x = [n1, n2]
            x.sort()
            n1 = x[0]
            n2 = x[1]
        elif isinstance(n2, TerminalNode):  # one is term node? n1 should be the term node
            n1, n2 = n2, n1
        self.n1 = n1
        self.n2 = n2

    def other_end(self, nid: Union[SyntenyNode, TerminalNode]):
        if nid == self.n1:
            return self.n2
        elif nid == self.n2:
            return self.n1
        else:
            raise ValueError('???')

    def has_term_node(self):
        return isinstance(self.n1, TerminalNode) or self.n2 is isinstance(self.n2, TerminalNode)

    def __eq__(self, other):
        return self.n1 == other.n1 and self.n2 == other.n2

    def __hash__(self):
        return hash((self.n1, self.n2))

    def __str__(self):
        return str((self.n1, self.n2))

    def __repr__(self):
        return str(self)
