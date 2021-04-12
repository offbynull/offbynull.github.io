from __future__ import annotations

from math import cos, pi, sin
from typing import List, Dict

from breakpoint_graph.ColoredEdge import ColoredEdge
from breakpoint_graph.Node import Node
from breakpoint_graph.SyntenyEdge import SyntenyEdge
from breakpoint_graph.SyntenyEnd import SyntenyEnd
from helpers.Utils import slide_window


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
    def __init__(self, red_p_list: List[List[str]], blue_p_list: List[List[str]]):
        # Node blue edge lookup
        node_to_blue_edges = {}
        for p in blue_p_list:
            for (s1, s2), idx in slide_window(p, 2, cyclic=True):
                if s1[0] == '-' and s2[0] == '+':
                    n1 = Node(s1[1:], SyntenyEnd.HEAD)
                    n2 = Node(s2[1:], SyntenyEnd.HEAD)
                elif s1[0] == '+' and s2[0] == '-':
                    n1 = Node(s1[1:], SyntenyEnd.TAIL)
                    n2 = Node(s2[1:], SyntenyEnd.TAIL)
                elif s1[0] == '+' and s2[0] == '+':
                    n1 = Node(s1[1:], SyntenyEnd.TAIL)
                    n2 = Node(s2[1:], SyntenyEnd.HEAD)
                elif s1[0] == '-' and s2[0] == '-':
                    n1 = Node(s1[1:], SyntenyEnd.HEAD)
                    n2 = Node(s2[1:], SyntenyEnd.TAIL)
                else:
                    raise ValueError('???')
                e = ColoredEdge(n1, n2)
                node_to_blue_edges[n1] = e
                node_to_blue_edges[n2] = e

        # Node red edge lookup
        node_to_red_edges = {}
        for p in red_p_list:
            for (s1, s2), idx in slide_window(p, 2, cyclic=True):
                if s1[0] == '-' and s2[0] == '+':
                    n1 = Node(s1[1:], SyntenyEnd.HEAD)
                    n2 = Node(s2[1:], SyntenyEnd.HEAD)
                elif s1[0] == '+' and s2[0] == '-':
                    n1 = Node(s1[1:], SyntenyEnd.TAIL)
                    n2 = Node(s2[1:], SyntenyEnd.TAIL)
                elif s1[0] == '+' and s2[0] == '+':
                    n1 = Node(s1[1:], SyntenyEnd.TAIL)
                    n2 = Node(s2[1:], SyntenyEnd.HEAD)
                elif s1[0] == '-' and s2[0] == '-':
                    n1 = Node(s1[1:], SyntenyEnd.HEAD)
                    n2 = Node(s2[1:], SyntenyEnd.TAIL)
                else:
                    raise ValueError('???')
                e = ColoredEdge(n1, n2)
                node_to_red_edges[n1] = e
                node_to_red_edges[n2] = e

        # Because blue/red edges are undirected, you don't know which direction to traverse the graph when dumping out
        # the list of lists (permutations). This block caches the original input of synteny edges, such that you know
        # the correct direction to walk in.
        node_to_synteny_edge = {}
        for p in blue_p_list:
            for s in p:
                if s[0] == '+':
                    n1 = Node(s[1:], SyntenyEnd.HEAD)
                    n2 = Node(s[1:], SyntenyEnd.TAIL)
                elif s[0] == '-':
                    n1 = Node(s[1:], SyntenyEnd.TAIL)
                    n2 = Node(s[1:], SyntenyEnd.HEAD)
                else:
                    raise ValueError('???')
                e = SyntenyEdge(n1, n2)
                node_to_synteny_edge[n1] = e
                node_to_synteny_edge[n2] = e

        self.node_to_blue_edges = node_to_blue_edges
        self.node_to_red_edges = node_to_red_edges
        self.node_to_synteny_edge = node_to_synteny_edge

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

    def get_blue_permutations(self) -> List[List[str]]:
        return self._walk_to_permutations(self.node_to_blue_edges.copy())

    def get_red_permutations(self) -> List[List[str]]:
        return self._walk_to_permutations(self.node_to_red_edges.copy())

    def _walk_to_permutations(self, remaining: Dict[Node, ColoredEdge]) -> List[List[str]]:
        ret = []
        while (nid := next(iter(remaining), None)) is not None:
            # output in the direction in which perms were originally input by starting from the destination of the
            # synteny edge that nid is for
            nid = self.node_to_synteny_edge[nid].n2
            p = []
            while nid in remaining:
                edge = remaining[nid]
                # remove both ends of synteny block to avoid walking it again
                del remaining[nid]
                del remaining[nid.other_end()]
                other_nid = edge.get_other_node(nid)
                if other_nid.end == SyntenyEnd.HEAD:
                    p += ['+' + other_nid.id]
                elif other_nid.end == SyntenyEnd.TAIL:
                    p += ['-' + other_nid.id]
                else:
                    raise ValueError('???')
                nid = Node(other_nid.id, other_nid.end.swap())
            ret.append(p)
        return ret

    def _ordered_walk_over_synteny_edges(self):  # in this case, ordered means ordered by blue edges
        remaining = self.node_to_blue_edges.copy()
        nid = next(iter(remaining))
        while True:
            while nid in remaining:
                edge = remaining[nid]
                # remove both ends of synteny block to avoid walking it again
                del remaining[nid]
                del remaining[nid.other_end()]
                other_nid = edge.get_other_node(nid)
                if other_nid.end == SyntenyEnd.HEAD:
                    yield Node(other_nid.id, SyntenyEnd.HEAD), Node(other_nid.id, SyntenyEnd.TAIL)
                elif other_nid.end == SyntenyEnd.TAIL:
                    yield Node(other_nid.id, SyntenyEnd.TAIL), Node(other_nid.id, SyntenyEnd.HEAD)
                else:
                    raise ValueError('???')
                nid = other_nid.other_end()
            if remaining:
                nid = next(iter(remaining))
            else:
                break

    def to_neato_graph(self):
        g = ''
        g += 'graph G {\n'
        g += 'node [shape=plain];\n'
        # set node locations
        node_count = len(self.node_to_blue_edges)
        radius = node_count ** 1/4
        node_locations = [(cos(2 * pi / node_count * x) * radius, sin(2 * pi / node_count * x) * radius) for x in range(0, node_count + 1)]
        for n1, n2 in self._ordered_walk_over_synteny_edges():
            x1, y1 = node_locations.pop()
            x2, y2 = node_locations.pop()
            g += f'_{n1.id}_{n1.end.value}_ [pos="{x1},{y1}!"];\n'
            g += f'_{n2.id}_{n2.end.value}_ [pos="{x2},{y2}!"];\n'
        # set black edges representing synteny blocks
        for n1, n2 in self._ordered_walk_over_synteny_edges():
            g += f'_{n1.id}_{n1.end.value}_ -- _{n2.id}_{n2.end.value}_ [style=dashed, dir=forward];\n'
        # set blue edges (destination)
        for e in set(self.node_to_blue_edges.values()):
            g += f'_{e.n1.id}_{e.n1.end.value}_ -- _{e.n2.id}_{e.n2.end.value}_ [color=blue];\n'
        # draw red edges (source)
        for e in set(self.node_to_red_edges.values()):
            g += f'_{e.n1.id}_{e.n1.end.value}_ -- _{e.n2.id}_{e.n2.end.value}_ [color=red];\n'
        g += '}'
        return g


if __name__ == '__main__':
    bg = BreakpointGraph(
        [['+A', '-B', '-C', '+D'], ['+E']],
        [['+A', '+B', '-D'], ['-C', '-E']]
    )
    # graph is cyclic, so output permutations may start anywhere in the cycle
    # colored edges are undirected, so output permutations may come out negated+reversed
    print(f'{bg.get_red_permutations()}')
    print(f'{bg.get_blue_permutations()}')
    print(f'{bg.get_red_blue_cycles()}')
    print(f'{bg.to_neato_graph()}')