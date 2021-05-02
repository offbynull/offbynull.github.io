from __future__ import annotations
from enum import Enum
from math import cos, pi, sin
from typing import List, Dict

from helpers.Utils import slide_window

# DON'T USE THIS -- USE THE VERSION IN THE breakpoint_graph DIRECTORY INSTEAD
# DON'T USE THIS -- USE THE VERSION IN THE breakpoint_graph DIRECTORY INSTEAD
# DON'T USE THIS -- USE THE VERSION IN THE breakpoint_graph DIRECTORY INSTEAD
# DON'T USE THIS -- USE THE VERSION IN THE breakpoint_graph DIRECTORY INSTEAD
# DON'T USE THIS -- USE THE VERSION IN THE breakpoint_graph DIRECTORY INSTEAD
# DON'T USE THIS -- USE THE VERSION IN THE breakpoint_graph DIRECTORY INSTEAD
# DON'T USE THIS -- USE THE VERSION IN THE breakpoint_graph DIRECTORY INSTEAD
# DON'T USE THIS -- USE THE VERSION IN THE breakpoint_graph DIRECTORY INSTEAD
# DON'T USE THIS -- USE THE VERSION IN THE breakpoint_graph DIRECTORY INSTEAD
# DON'T USE THIS -- USE THE VERSION IN THE breakpoint_graph DIRECTORY INSTEAD
# DON'T USE THIS -- USE THE VERSION IN THE breakpoint_graph DIRECTORY INSTEAD
# DON'T USE THIS -- USE THE VERSION IN THE breakpoint_graph DIRECTORY INSTEAD
# DON'T USE THIS -- USE THE VERSION IN THE breakpoint_graph DIRECTORY INSTEAD
# DON'T USE THIS -- USE THE VERSION IN THE breakpoint_graph DIRECTORY INSTEAD
# DON'T USE THIS -- USE THE VERSION IN THE breakpoint_graph DIRECTORY INSTEAD
# DON'T USE THIS -- USE THE VERSION IN THE breakpoint_graph DIRECTORY INSTEAD
# DON'T USE THIS -- USE THE VERSION IN THE breakpoint_graph DIRECTORY INSTEAD
# DON'T USE THIS -- USE THE VERSION IN THE breakpoint_graph DIRECTORY INSTEAD
# DON'T USE THIS -- USE THE VERSION IN THE breakpoint_graph DIRECTORY INSTEAD
# DON'T USE THIS -- USE THE VERSION IN THE breakpoint_graph DIRECTORY INSTEAD
# DON'T USE THIS -- USE THE VERSION IN THE breakpoint_graph DIRECTORY INSTEAD
# DON'T USE THIS -- USE THE VERSION IN THE breakpoint_graph DIRECTORY INSTEAD
# DON'T USE THIS -- USE THE VERSION IN THE breakpoint_graph DIRECTORY INSTEAD
# DON'T USE THIS -- USE THE VERSION IN THE breakpoint_graph DIRECTORY INSTEAD
# DON'T USE THIS -- USE THE VERSION IN THE breakpoint_graph DIRECTORY INSTEAD
# DON'T USE THIS -- USE THE VERSION IN THE breakpoint_graph DIRECTORY INSTEAD
# DON'T USE THIS -- USE THE VERSION IN THE breakpoint_graph DIRECTORY INSTEAD
# DON'T USE THIS -- USE THE VERSION IN THE breakpoint_graph DIRECTORY INSTEAD
# DON'T USE THIS -- USE THE VERSION IN THE breakpoint_graph DIRECTORY INSTEAD
# DON'T USE THIS -- USE THE VERSION IN THE breakpoint_graph DIRECTORY INSTEAD
# DON'T USE THIS -- USE THE VERSION IN THE breakpoint_graph DIRECTORY INSTEAD
# DON'T USE THIS -- USE THE VERSION IN THE breakpoint_graph DIRECTORY INSTEAD
# DON'T USE THIS -- USE THE VERSION IN THE breakpoint_graph DIRECTORY INSTEAD
# DON'T USE THIS -- USE THE VERSION IN THE breakpoint_graph DIRECTORY INSTEAD
# DON'T USE THIS -- USE THE VERSION IN THE breakpoint_graph DIRECTORY INSTEAD
# DON'T USE THIS -- USE THE VERSION IN THE breakpoint_graph DIRECTORY INSTEAD
# DON'T USE THIS -- USE THE VERSION IN THE breakpoint_graph DIRECTORY INSTEAD
# DON'T USE THIS -- USE THE VERSION IN THE breakpoint_graph DIRECTORY INSTEAD
# DON'T USE THIS -- USE THE VERSION IN THE breakpoint_graph DIRECTORY INSTEAD
# DON'T USE THIS -- USE THE VERSION IN THE breakpoint_graph DIRECTORY INSTEAD
# DON'T USE THIS -- USE THE VERSION IN THE breakpoint_graph DIRECTORY INSTEAD
# DON'T USE THIS -- USE THE VERSION IN THE breakpoint_graph DIRECTORY INSTEAD
# DON'T USE THIS -- USE THE VERSION IN THE breakpoint_graph DIRECTORY INSTEAD
# DON'T USE THIS -- USE THE VERSION IN THE breakpoint_graph DIRECTORY INSTEAD
# DON'T USE THIS -- USE THE VERSION IN THE breakpoint_graph DIRECTORY INSTEAD
# DON'T USE THIS -- USE THE VERSION IN THE breakpoint_graph DIRECTORY INSTEAD
# DON'T USE THIS -- USE THE VERSION IN THE breakpoint_graph DIRECTORY INSTEAD
# DON'T USE THIS -- USE THE VERSION IN THE breakpoint_graph DIRECTORY INSTEAD
# DON'T USE THIS -- USE THE VERSION IN THE breakpoint_graph DIRECTORY INSTEAD
# DON'T USE THIS -- USE THE VERSION IN THE breakpoint_graph DIRECTORY INSTEAD
# DON'T USE THIS -- USE THE VERSION IN THE breakpoint_graph DIRECTORY INSTEAD
# DON'T USE THIS -- USE THE VERSION IN THE breakpoint_graph DIRECTORY INSTEAD
# DON'T USE THIS -- USE THE VERSION IN THE breakpoint_graph DIRECTORY INSTEAD
# DON'T USE THIS -- USE THE VERSION IN THE breakpoint_graph DIRECTORY INSTEAD
# DON'T USE THIS -- USE THE VERSION IN THE breakpoint_graph DIRECTORY INSTEAD
# DON'T USE THIS -- USE THE VERSION IN THE breakpoint_graph DIRECTORY INSTEAD
# DON'T USE THIS -- USE THE VERSION IN THE breakpoint_graph DIRECTORY INSTEAD
# DON'T USE THIS -- USE THE VERSION IN THE breakpoint_graph DIRECTORY INSTEAD
# DON'T USE THIS -- USE THE VERSION IN THE breakpoint_graph DIRECTORY INSTEAD

class SyntenyEnd(Enum):
    HEAD = 'h'
    TAIL = 't'

    def __lt__(self, other):
        return self.value < other.value

    def __str__(self):
        return self.value

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

    def __repr__(self):
        return str(self)


class ColoredEdge:
    def __init__(self, n1: Node, n2: Node):
        assert n1 != n2
        x = [n1, n2]
        x.sort()
        self.n1 = x[0]
        self.n2 = x[1]

    def get_other_node(self, nid: Node):
        if nid == self.n1:
            return self.n2
        elif nid == self.n2:
            return self.n1
        else:
            raise ValueError('???')

    def __eq__(self, other):
        return self.n1 == other.n1 and self.n2 == other.n2

    def __hash__(self):
        return hash((self.n1, self.n2))

    def __str__(self):
        return str((self.n1, self.n2))

    def __repr__(self):
        return str(self)


# This class only holds on to the...
#
#  * blue edges (representing the graph you're trying to reach -- the good state)
#  * red edges (representing the graph you're starting from -- the bad state)
#
# ..., not the synteny edges themselves. The synteny edges in the breakpoint graph are for the good state (blue edges),
# meaning that the blue edges will ALWAYS sandwiched between the synteny edges. As such, the synteny edges can be
# derived directly from the blue edges. For example, given the blue_p_list of [+A, -B, -C, +D], the implied synteny
# edges are...
#
#  * +A: Ahead--------->Atail
#  * -B: Btail<---------Bhead
#  * -C  Ctail<---------Chead
#  * +D  Dhead--------->Dtail
#
# The direction of the synteny block just dictates which end (head or tail) shows up first. These ends are linked
# back-to-back with blue edges.
#
#       Ah---->At
#     b           b
#    b             b
#  Dt               Bt
#   ^               ^
#   |               |
#  Dh               Bh
#    b             b
#     b           b
#       Ch---->Ct
class BreakpointGraph:
    def __init__(self, red_p_list: List[List[int]], blue_p_list: List[List[int]]):
        # Node blue edge lookup
        node_to_blue_edges = {}
        for p in blue_p_list:
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
                e = ColoredEdge(n1, n2)
                node_to_blue_edges[n1] = e
                node_to_blue_edges[n2] = e

        # Node red edge lookup
        node_to_red_edges = {}
        for p in red_p_list:
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
                e = ColoredEdge(n1, n2)
                node_to_red_edges[n1] = e
                node_to_red_edges[n2] = e

        self.node_to_blue_edges = node_to_blue_edges
        self.node_to_red_edges = node_to_red_edges

        # Because the red/blue edges are undirected, the start_nid defines which node to start from when traversing the
        # graph from when dumping out the graph back into a list of lists (permutations).
        if red_p_list[0][0] > 0:
            self.start_nid = Node(red_p_list[0][0], SyntenyEnd.TAIL)
        elif red_p_list[0][0] < 0:
            self.start_nid = Node(-red_p_list[0][0], SyntenyEnd.HEAD)
        else:
            raise ValueError('???')

    def find_blue_edge_in_non_trivial_cycle(self):
        for nid in self.node_to_blue_edges:
            blue_edge = self.node_to_blue_edges[nid]
            red_edge = self.node_to_red_edges[nid]
            if blue_edge != red_edge:
                return blue_edge
        return None

    def get_red_blue_cycles(self):
        remaining_nids = set(self.node_to_blue_edges.keys())
        next_nid = next(iter(remaining_nids))
        remaining_nids.remove(next_nid)
        mode = 'blue'
        cycles = []
        cycle = [next_nid]
        while True:
            if mode == 'blue':
                edge = self.node_to_blue_edges[next_nid]
                mode = 'red'
            elif mode == 'red':
                edge = self.node_to_red_edges[next_nid]
                mode = 'blue'
            else:
                raise ValueError('???')
            next_nid = edge.get_other_node(next_nid)
            if not remaining_nids:  # this cycle has finished + there are more remaining ids to walk over
                cycles.append(cycle)
                break
            if next_nid not in remaining_nids:  # this cycle has finished, move on to the next cycle
                cycles.append(cycle)
                cycle = []
                next_nid = next(iter(remaining_nids))
                remaining_nids.remove(next_nid)
            else:   # this cycle has NOT finished, keep to the next node
                cycle.append(next_nid)
                remaining_nids.remove(next_nid)
        return cycles

    def apply_2break(self, blue_edge: ColoredEdge):
        red_edge_1 = self.node_to_red_edges[blue_edge.n1]
        red_edge_2 = self.node_to_red_edges[blue_edge.n2]
        if blue_edge == red_edge_1 == red_edge_2:
            raise ValueError('Already in trivial cycle')
        nid1 = blue_edge.n1
        nid2 = red_edge_1.get_other_node(blue_edge.n1)
        nid3 = blue_edge.n2
        nid4 = red_edge_2.get_other_node(blue_edge.n2)
        del self.node_to_red_edges[nid1]
        del self.node_to_red_edges[nid2]
        del self.node_to_red_edges[nid3]
        del self.node_to_red_edges[nid4]
        self.node_to_red_edges[nid1] = ColoredEdge(nid1, nid3)
        self.node_to_red_edges[nid3] = ColoredEdge(nid1, nid3)
        self.node_to_red_edges[nid2] = ColoredEdge(nid2, nid4)
        self.node_to_red_edges[nid4] = ColoredEdge(nid2, nid4)

    def get_blue_permutations(self) -> List[List[int]]:
        return self._walk_to_permutations(self.node_to_blue_edges.copy())

    def get_red_permutations(self) -> List[List[int]]:
        return self._walk_to_permutations(self.node_to_red_edges.copy())

    def _walk_to_permutations(self, remaining: Dict[Node, ColoredEdge]) -> List[List[int]]:
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

    def _ordered_walk_over_synteny_edges(self):
        next_nid = self.start_nid
        while True:
            blue_edge = self.node_to_blue_edges[next_nid]
            other_nid = blue_edge.get_other_node(next_nid)
            if other_nid.end == SyntenyEnd.HEAD:
                yield Node(other_nid.id, SyntenyEnd.HEAD), Node(other_nid.id, SyntenyEnd.TAIL)
            elif other_nid.end == SyntenyEnd.TAIL:
                yield Node(other_nid.id, SyntenyEnd.TAIL), Node(other_nid.id, SyntenyEnd.HEAD)
            else:
                raise ValueError('???')
            next_nid = other_nid.other_end()
            if next_nid == self.start_nid:
                break

    def _ordered_walk_over_blue_edges(self):
        next_nid = self.start_nid
        while True:
            blue_edge = self.node_to_blue_edges[next_nid]
            yield blue_edge
            other_nid = blue_edge.get_other_node(next_nid)
            next_nid = other_nid.other_end()
            if next_nid == self.start_nid:
                break

    def to_neato_graph(self):
        g = ''
        g += 'graph G {\n'
        g += 'node [shape=plain];\n'

        node_count = len(self.node_to_blue_edges)
        radius = node_count ** 1/4
        node_locations = [(cos(2 * pi / node_count * x) * radius, sin(2 * pi / node_count * x) * radius) for x in range(0, node_count + 1)]

        # Set node locations
        for n1, n2 in self._ordered_walk_over_synteny_edges():
            x1, y1 = node_locations.pop()
            x2, y2 = node_locations.pop()
            g += f'_{n1.id}{n1.end.value}_ [pos="{x1},{y1}!"];\n'
            g += f'_{n2.id}{n2.end.value}_ [pos="{x2},{y2}!"];\n'

        # Set black edges representing synteny blocks
        for n1, n2 in self._ordered_walk_over_synteny_edges():
            g += f'_{n1.id}{n1.end.value}_ -- _{n2.id}{n2.end.value}_ [style=dashed, dir=forward];\n'

        # Set blue edges (destination)
        for e in self._ordered_walk_over_blue_edges():
            g += f'_{e.n1.id}{e.n1.end.value}_ -- _{e.n2.id}{e.n2.end.value}_ [color=blue];\n'

        # Draw red edges (source)
        for e in set(self.node_to_red_edges.values()):
            g += f'_{e.n1.id}{e.n1.end.value}_ -- _{e.n2.id}{e.n2.end.value}_ [color=red];\n'

        g += '}'

        return g


if __name__ == '__main__':
    bg = BreakpointGraph(
        [[+1, -2, -3, +4]],
        [[+1, +2, -4, -3]]
        # [[+9, -8, +12, +7, +1, -14, +13, +3, -5, -11, +6, -2, +10, -4]],
        # [[-11, +8, -10, -2, +3, +4, +13, +6, +12, +9, +5, +7, -14, -1]]
    )
    print(f'{bg.get_red_blue_cycles()}')
    # print(f'STARTING FROM {bg.get_red_permutations()} AND GOING TO {bg.get_blue_permutations()}')
    # print(f'{bg.to_neato_graph()}')
    # print('----------------')
    # while True:
    #     next_blue_edge_to_break_on = bg.find_blue_edge_in_non_trivial_cycle()
    #     if next_blue_edge_to_break_on is None:
    #         break
    #     bg.apply_2break(next_blue_edge_to_break_on)
    #     print(f'{bg.get_red_permutations()}')
    #     print(f'{bg.to_neato_graph()}')