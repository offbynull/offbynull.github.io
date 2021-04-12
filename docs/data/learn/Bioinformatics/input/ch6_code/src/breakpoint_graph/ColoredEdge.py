from typing import Optional

from breakpoint_graph.Node import Node


class ColoredEdge:
    def __init__(self, n1: Optional[Node], n2: Optional[Node]):
        assert n1 != n2
        if n1 and n2:
            x = [n1, n2]
            x.sort()
            n1: Optional[Node] = x[0]
            n2: Optional[Node] = x[1]
        elif not n1 and not n2:
            raise ValueError('At least one must be not None')
        self.n1: Optional[Node] = n1
        self.n2: Optional[Node] = n2

    def get_other_node(self, nid: Optional[Node]):
        if nid == self.n1:
            return self.n2
        elif nid == self.n2:
            return self.n1
        else:
            raise ValueError('???')

    def is_term(self):
        return self.n1 is None or self.n2 is None

    def __eq__(self, other):
        return self.n1 == other.n1 and self.n2 == other.n2

    def __hash__(self):
        return hash((self.n1, self.n2))

    def __str__(self):
        return str((self.n1, self.n2))

    def __repr__(self):
        return str(self)