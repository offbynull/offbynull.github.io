from __future__ import annotations
from enum import Enum
from math import cos, pi, sin
from typing import List, Dict

from helpers.Utils import slide_window


class SyntenyEnd(Enum):
    HEAD = 'h'
    TAIL = 't'

    def __lt__(self, other):
        return self.value < other.value

    def swap(self) -> SyntenyEnd:
        if self == SyntenyEnd.HEAD:
            return SyntenyEnd.TAIL
        else:
            return SyntenyEnd.HEAD


class Node:
    def __init__(self, id: int, end: SyntenyEnd):
        assert id > 0
        self.id = id
        self.end = end

    def other_end(self) -> Node:
        return Node(self.id, self.end.swap())

    def __lt__(self, other):
        if self.id < other.id:
            return True
        elif self.id == other.id and self.end < other.end:
            return True
        else:
            return False

    def __eq__(self, other):
        return self.id == other.id and self.end == other.end

    def __hash__(self):
        return hash((self.id, self.end))

    def __str__(self):
        return str((self.id, self.end))


class Color(Enum):
    RED = 'red'
    BLUE = 'blue'


class ColoredEdge:
    def __init__(self, n1: Node, n2: Node, color: Color):
        assert n1 != n2
        x = [n1, n2]
        x.sort()
        self.n1 = x[0]
        self.n2 = x[1]
        self.color = color

    def get_other_node(self, nid: Node):
        if nid == self.n1:
            return self.n2
        elif nid == self.n2:
            return self.n1
        else:
            raise ValueError('???')


class BreakpointGraph:
    def __init__(self, src: List[List[int]], dst: List[List[int]]):
        # Node blue edge lookup
        node_to_blue_edges = {}
        for p in src:
            for (s1, s2), idx in slide_window(p, 2, cyclic=True):
                if s1 < 0 and s2 > 0:
                    n1 = Node(-s1, SyntenyEnd.HEAD)
                    n2 = Node(s2, SyntenyEnd.HEAD)
                elif s1 > 0 and s2 < 0:
                    n1 = Node(s1, SyntenyEnd.TAIL)
                    n2 = Node(-s2, SyntenyEnd.TAIL)
                elif s1 > 0 and s2 > 0:
                    n1 = Node(s1, SyntenyEnd.TAIL)
                    n2 = Node(s2, SyntenyEnd.HEAD)
                elif s1 < 0 and s2 < 0:
                    n1 = Node(-s1, SyntenyEnd.HEAD)
                    n2 = Node(-s2, SyntenyEnd.TAIL)
                else:
                    raise ValueError('???')
                e = ColoredEdge(n1, n2, Color.BLUE)
                node_to_blue_edges[n1] = e
                node_to_blue_edges[n2] = e

        # Node red edge lookup
        node_to_red_edges = {}
        for p in dst:
            for (s1, s2), idx in slide_window(p, 2, cyclic=True):
                if s1 < 0 and s2 > 0:
                    n1 = Node(-s1, SyntenyEnd.HEAD)
                    n2 = Node(s2, SyntenyEnd.HEAD)
                elif s1 > 0 and s2 < 0:
                    n1 = Node(s1, SyntenyEnd.TAIL)
                    n2 = Node(-s2, SyntenyEnd.TAIL)
                elif s1 > 0 and s2 > 0:
                    n1 = Node(s1, SyntenyEnd.TAIL)
                    n2 = Node(s2, SyntenyEnd.HEAD)
                elif s1 < 0 and s2 < 0:
                    n1 = Node(-s1, SyntenyEnd.HEAD)
                    n2 = Node(-s2, SyntenyEnd.TAIL)
                else:
                    raise ValueError('???')
                e = ColoredEdge(n1, n2, Color.RED)
                node_to_red_edges[n1] = e
                node_to_red_edges[n2] = e

        self.node_to_blue_edges = node_to_blue_edges
        self.node_to_red_edges = node_to_red_edges
        if src[0][0] > 0:
            self.start_nid = Node(src[0][0], SyntenyEnd.TAIL)
        elif src[0][0] < 0:
            self.start_nid = Node(src[0][0], SyntenyEnd.HEAD)
        else:
            raise ValueError('???')

    def get_source(self) -> List[List[int]]:
        return self._walk_to_synteny_blocks(self.node_to_blue_edges.copy())

    def get_destination(self) -> List[List[int]]:
        return self._walk_to_synteny_blocks(self.node_to_red_edges.copy())

    def _walk_to_synteny_blocks(self, remaining: Dict[Node, ColoredEdge]) -> List[List[int]]:
        ret = []
        nid = self.start_nid
        while True:
            p = []
            while nid in remaining:
                edge = remaining[nid]
                # remove both ends of synteny block to avoid walking it again
                del remaining[nid]
                del remaining[nid.other_end()]
                other_nid = edge.get_other_node(nid)
                if other_nid.end == SyntenyEnd.HEAD:
                    p += [other_nid.id]
                elif other_nid.end == SyntenyEnd.TAIL:
                    p += [-other_nid.id]
                else:
                    raise ValueError('???')
                nid = Node(other_nid.id, other_nid.end.swap())
            ret.append(p)
            if remaining:
                nid = next(iter(remaining))
            else:
                break
        return ret

    def to_neato_graph(self):
        src = self.get_source()
        dst = self.get_destination()

        g = ''
        g += 'graph G {\n'
        g += 'node [shape=plain];\n'

        node_count = sum(len(p) for p in src) * 2
        radius = node_count ** 1/4
        node_locations = [(cos(2 * pi / node_count * x) * radius, sin(2 * pi / node_count * x) * radius) for x in range(0, node_count + 1)]

        for p in src:
            for s in p:
                x1, y1 = node_locations.pop()
                x2, y2 = node_locations.pop()
                if s > 0:
                    g += f'_{s}h_ [pos="{x1},{y1}!"];\n'
                    g += f'_{s}t_ [pos="{x2},{y2}!"];\n'
                elif s < 0:
                    g += f'_{-s}t_ [pos="{x1},{y1}!"];\n'
                    g += f'_{-s}h_ [pos="{x2},{y2}!"];\n'

        # Draw black edges
        for p in src:
            for s in p:
                if s > 0:
                    g += f'_{s}h_ -- _{s}t_ [style=dashed, dir=forward];\n'
                elif s < 0:
                    g += f'_{-s}t_ -- _{-s}h_ [style=dashed, dir=back];\n'
                else:
                    raise ValueError('???')

        # Draw blue edges (source)
        for p in src:
            for (s1, s2), idx in slide_window(p, 2, cyclic=True):
                if s1 < 0 and s2 > 0:
                    g += f'_{-s1}h_ -- _{s2}h_ [color=blue];\n'
                elif s1 > 0 and s2 < 0:
                    g += f'_{s1}t_ -- _{-s2}t_ [color=blue];\n'
                elif s1 > 0 and s2 > 0:
                    g += f'_{s1}t_ -- _{s2}h_ [color=blue];\n'
                elif s1 < 0 and s2 < 0:
                    g += f'_{-s1}h_ -- _{-s2}t_ [color=blue];\n'
                else:
                    raise ValueError('???')

        # Draw red edges (destination)
        for p in dst:
            for (s1, s2), idx in slide_window(p, 2, cyclic=True):
                if s1 < 0 and s2 > 0:
                    g += f'_{-s1}h_ -- _{s2}h_ [color=red];\n'
                elif s1 > 0 and s2 < 0:
                    g += f'_{s1}t_ -- _{-s2}t_ [color=red];\n'
                elif s1 > 0 and s2 > 0:
                    g += f'_{s1}t_ -- _{s2}h_ [color=red];\n'
                elif s1 < 0 and s2 < 0:
                    g += f'_{-s1}h_ -- _{-s2}t_ [color=red];\n'
                else:
                    raise ValueError('???')

        g += '}'

        return g


if __name__ == '__main__':
    bg = BreakpointGraph(
        [[+9, -8, +12], [+13, +3, +4, -10, +2, -6, +11, +1, +14], [+5, +7]],
        [[+9, -8, +12, +7, +1, -14, +13, +3, -5, -11, +6, -2, +10, -4]]
    )
    print(f'{bg.get_source()}')
    print(f'{bg.get_destination()}')
    print(f'{bg.to_neato_graph()}')