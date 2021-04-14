from typing import Optional, Dict, Set, Union

from breakpoint_graph.ColoredEdge import ColoredEdge
from breakpoint_graph.SyntenyNode import SyntenyNode
from breakpoint_graph.TerminalNode import TerminalNode


class ColoredEdgeSet:
    def __init__(self):
        self.by_node: Dict[SyntenyNode, ColoredEdge] = {}

    def insert(self, e: ColoredEdge):
        if e.n1 in self.by_node or e.n2 in self.by_node:
            raise ValueError(f'Node already occupied: {e}')
        if not isinstance(e.n1, TerminalNode):
            self.by_node[e.n1] = e
        if not isinstance(e.n2, TerminalNode):
            self.by_node[e.n2] = e

    def find(self, n: Union[SyntenyNode, TerminalNode]) -> Optional[ColoredEdge]:
        return self.by_node.get(n, None)

    def find_all(self, *n: Union[SyntenyNode, TerminalNode]) -> Set[ColoredEdge]:
        ret = set()
        for _n in n:
            found = self.find(_n)
            if found is not None:
                ret.add(found)
        return ret

    def remove(self, n: SyntenyNode) -> Optional[ColoredEdge]:
        return self.by_node.pop(n, None)

    def remove_edge(self, e: ColoredEdge) -> None:
        if not isinstance(e.n1, TerminalNode):
            found_e = self.find(e.n1)
        elif not isinstance(e.n2, TerminalNode):
            found_e = self.find(e.n2)
        else:
            raise ValueError('???')
        if found_e != e:
            raise ValueError('Edge doesn\'t exist')
        if not isinstance(e.n1, TerminalNode):
            del self.by_node[e.n1]
        if not isinstance(e.n2, TerminalNode):
            del self.by_node[e.n2]

    def nodes(self) -> Set[SyntenyNode]:
        return set(self.by_node.keys())

    def edges(self) -> Set[ColoredEdge]:
        return set(self.by_node.values())
