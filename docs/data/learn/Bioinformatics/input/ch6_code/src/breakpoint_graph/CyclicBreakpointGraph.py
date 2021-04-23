from __future__ import annotations

from math import cos, pi, sin
from typing import List

from breakpoint_graph.ColoredEdge import ColoredEdge
from breakpoint_graph.ColoredEdgeSet import ColoredEdgeSet
from breakpoint_graph.Permutation import Permutation
from breakpoint_graph.SyntenyEdge import SyntenyEdge


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
from breakpoint_graph.SyntenyEnd import SyntenyEnd


class BreakpointGraph:
    def __init__(self, red_p_list: List[List[str]], blue_p_list: List[List[str]]):
        self.blue_edges = ColoredEdgeSet.create(
            ce for p in blue_p_list for ce in Permutation.from_raw(p, True).to_colored_edges()
        )
        self.red_edges = ColoredEdgeSet.create(
            ce for p in red_p_list for ce in Permutation.from_raw(p, True).to_colored_edges()
        )

    def get_red_blue_paths(self):
        remaining_n_set = self.blue_edges.nodes()
        paths = []
        while remaining_n_set:
            orig_n = remaining_n_set.pop()
            walked_n_set = set()
            path = ColoredEdgeSet.alternating_walk(orig_n, 0, [self.blue_edges, self.red_edges], walked_n_set)
            paths += [path]
            remaining_n_set.difference_update(walked_n_set)
        return paths

    def find_blue_edge_in_non_trivial_path(self):
        for n in self.blue_edges.nodes():
            blue_edge = self.blue_edges.find(n)
            red_edge = self.red_edges.find(n)
            if blue_edge != red_edge:
                return blue_edge
        return None

    def two_break(self, blue_edge: ColoredEdge):
        red_edge1 = self.red_edges.remove(blue_edge.n1)
        red_edge2 = self.red_edges.remove(blue_edge.n2)
        # Given that you want one of the new red_edges to match blue_edge, this will return the OTHER new red edge. That
        # is, it'll swap the ends of the existing red edges such that one of the new red_edges is blue_edge and the
        # other new red_edge gets returned.
        new_red_edge = ColoredEdge.swap_ends(red_edge1, red_edge2, blue_edge)
        self.red_edges.insert(blue_edge)
        self.red_edges.insert(new_red_edge)

    def get_blue_permutations(self) -> List[List[str]]:
        return BreakpointGraph._walk_to_permutations(self.blue_edges)

    def get_red_permutations(self) -> List[List[str]]:
        return BreakpointGraph._walk_to_permutations(self.red_edges)

    @staticmethod
    def _walk_to_permutations(colored_edges: ColoredEdgeSet) -> List[List[str]]:
        remaining = colored_edges.edges()
        perms = []
        while remaining:
            e = remaining.pop()
            p, walked_ce_set = Permutation.from_colored_edges(colored_edges, e.n1, True)
            p_raw = p.to_normalized_raw()
            perms.append(p_raw)
            remaining.difference_update(walked_ce_set)
        return perms

    def to_neato_graph(self):
        blue_edges = self.blue_edges.edges()
        red_edges = self.red_edges.edges()
        syn_edges = [edge for edges in self.blue_edges.walk() for edge in edges if isinstance(edge, SyntenyEdge)]
        g = ''
        g += 'graph G {\n'
        g += 'layout=neato\n'
        g += 'node [shape=plain];\n'
        # set node locations
        node_count = len(syn_edges) * 2
        radius = node_count ** 1/4
        node_locations = [(cos(2 * pi / node_count * x) * radius, sin(2 * pi / node_count * x) * radius) for x in range(0, node_count + 1)]
        for s in syn_edges:
            n1 = s.n1
            n2 = s.n2
            x1, y1 = node_locations.pop()
            x2, y2 = node_locations.pop()
            g += f'_{n1.id}_{n1.end.value}_ [pos="{x1},{y1}!"];\n'
            g += f'_{n2.id}_{n2.end.value}_ [pos="{x2},{y2}!"];\n'
        # set black edges representing synteny blocks
        for s in syn_edges:
            n1 = s.n1
            n2 = s.n2
            dir = 'forward' if n1.end == SyntenyEnd.HEAD else 'back'
            g += f'_{n1.id}_{n1.end.value}_ -- _{n2.id}_{n2.end.value}_ [style=dashed, dir={dir}];\n'
        # set blue edges (destination)
        for e in blue_edges:
            g += f'_{e.n1.id}_{e.n1.end.value}_ -- _{e.n2.id}_{e.n2.end.value}_ [color=blue];\n'
        # draw red edges (source)
        for e in red_edges:
            g += f'_{e.n1.id}_{e.n1.end.value}_ -- _{e.n2.id}_{e.n2.end.value}_ [color=red];\n'
        g += '}'
        return g


if __name__ == '__main__':
    bg = BreakpointGraph(
        [['+A', '-B', '-C', '+D'], ['+E']],
        [['+A', '+B', '-D'], ['-C', '-E']]
    )
    while (next_blue_edge := bg.find_blue_edge_in_non_trivial_path()) is not None:
        print(f'{bg.get_red_permutations()}')
        print(f'{bg.get_blue_permutations()}')
        print(f'{bg.get_red_blue_paths()}')
        print(f'{bg.to_neato_graph()}')
        bg.two_break(next_blue_edge)
    print(f'{bg.get_red_permutations()}')
    print(f'{bg.get_blue_permutations()}')
    print(f'{bg.get_red_blue_paths()}')
    print(f'{bg.to_neato_graph()}')
