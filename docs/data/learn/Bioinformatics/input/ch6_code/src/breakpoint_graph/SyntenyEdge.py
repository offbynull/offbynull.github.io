from __future__ import annotations

from typing import Tuple

from breakpoint_graph.Node import Node
from breakpoint_graph.SyntenyEnd import SyntenyEnd


class SyntenyEdge:
    def __init__(self, n1: Node, n2: Node):
        assert n1.id == n2.id
        assert n1.end != n2.end
        self.n1 = n1
        self.n2 = n2

    @staticmethod
    def from_str(v: str) -> Tuple[SyntenyEdge, str]:
        if v[0] == '+':
            return SyntenyEdge(
                Node(v[1:], SyntenyEnd.HEAD),
                Node(v[1:], SyntenyEnd.TAIL)
            ), v[1:]
        elif v[0] == '-':
            return SyntenyEdge(
                Node(v[1:], SyntenyEnd.TAIL),
                Node(v[1:], SyntenyEnd.HEAD)
            ), v[1:]
        else:
            raise ValueError('???')

    @staticmethod
    def id(v: str) -> str:
        return v[1:]

    def __eq__(self, other):
        return self.n1 == other.n1 and self.n2 == other.n2

    def __hash__(self):
        return hash((self.n1, self.n2))

    def __str__(self):
        return str((self.n1, self.n2))

    def __repr__(self):
        return str(self)