from __future__ import annotations

from math import cos, pi, sin
from typing import List, Set

from breakpoint_graph.ColoredEdge import ColoredEdge
from breakpoint_graph.ColoredEdgeSet import ColoredEdgeSet
from breakpoint_graph.Permutation import Permutation
from breakpoint_graph.SyntenyEdge import SyntenyEdge
from breakpoint_graph.SyntenyEnd import SyntenyEnd
from breakpoint_graph.SyntenyNode import SyntenyNode
from breakpoint_graph.TerminalNode import TerminalNode
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
#             bbbb          bbbb          bbbb
#   Ah----->At    Bt<-----Bh    Ct<-----Ch    Dh----->Dt
class BreakpointGraph:
    def __init__(self, red_p_list: List[List[str]], blue_p_list: List[List[str]]):
        synteny_edges = []
        for p_num, p in enumerate(blue_p_list):
            for s in p:
                e, id = SyntenyEdge.from_str(s)
                synteny_edges.append(e)
        self.synteny_edges = synteny_edges
        self.blue_edges = BreakpointGraph._p_list_to_edges(blue_p_list)
        self.red_edges = BreakpointGraph._p_list_to_edges(red_p_list)

    @staticmethod
    def _p_list_to_edges(p_list: List[List[str]]) -> ColoredEdgeSet:
        ret = ColoredEdgeSet()
        for p in p_list:
            for ce in Permutation.from_raw(p, False).to_colored_edges():
                ret.insert(ce)
        return ret

    def _walk_red_blue(self, next_n: SyntenyNode, color: str, walked_n_set: Set[SyntenyNode]) -> List[SyntenyNode]:
        path = []
        while True:
            if color == 'blue':
                edge = self.blue_edges.find(next_n)
                color = 'red'
            elif color == 'red':
                edge = self.red_edges.find(next_n)
                color = 'blue'
            else:
                raise ValueError('???')
            path.append(next_n)
            walked_n_set.add(next_n)
            next_n = edge.other_end(next_n)
            if next_n == TerminalNode.INST:  # reached terminus (end of chromosome), flip and try going in other dir
                break
            if next_n in walked_n_set:  # reached loop
                break
        return path

    def get_red_blue_paths(self) -> List[List[SyntenyNode]]:
        remaining_n_set = self.blue_edges.nodes()
        paths = []
        while remaining_n_set:
            orig_n = remaining_n_set.pop()
            walked_n_set = set()
            from_blue = self._walk_red_blue(orig_n, 'blue', walked_n_set)
            from_red = self._walk_red_blue(orig_n, 'red', walked_n_set)
            remaining_n_set.difference_update(walked_n_set)
            # both from_blue and from_red will start with orig_id, so clip if off one of them (from_red in this case)
            # and reverse the other before concatenating
            path = from_blue[::-1] + from_red[1:]
            paths += [path]
        return paths

    def find_blue_edge_in_non_trivial_path(self):
        for p in self.get_red_blue_paths():
            if len(p) == 1:
                continue
            if len(p) == 2 and self.red_edges.find(p[0]) == self.red_edges.find(p[1]):
                continue
            return self.blue_edges.find(p[0])
        return None

    def apply_2break(self, blue_edge: ColoredEdge):
        red_edge1 = self.red_edges.remove(blue_edge.n1)  # If blue_edge.n1 is TERM, will return None
        red_edge2 = self.red_edges.remove(blue_edge.n2)  # If blue_edge.n2 is TERM, will return None
        # Given that you want one of the new red_edges to match blue_edge, this will return the OTHER new red edge. That
        # is, it'll swap the ends of the existing red edges such that one of the new red_edges is blue_edge and the
        # other new red_edge gets returned.
        new_red_edge = ColoredEdge.swap_ends(red_edge1, red_edge2, blue_edge)
        self.red_edges.insert(blue_edge)
        if new_red_edge:  # It's possible both ends for new_red_edge were TERM, in which case it'll be None
            self.red_edges.insert(new_red_edge)

    def get_blue_permutations(self) -> List[List[str]]:
        return BreakpointGraph._walk_to_permutations(self.blue_edges)

    def get_red_permutations(self) -> List[List[str]]:
        return BreakpointGraph._walk_to_permutations(self.red_edges)

    @staticmethod
    def _walk_to_permutations(colored_edges: ColoredEdgeSet) -> List[List[str]]:
        term_edges = set()
        for ce in colored_edges.edges():
            if ce.has_term():
                term_edges.add(ce)
        perms = []
        while term_edges:
            n = term_edges.pop().other_end(TerminalNode.INST)
            p, walked_ce_set = Permutation.from_colored_edges(colored_edges, n, False)
            p_raw = p.to_normalized_raw()
            perms.append(p_raw)
            term_edges.difference_update(walked_ce_set)
        return perms

    def to_neato_graph(self):
        g = ''
        g += 'graph G {\n'
        g += 'node [shape=plain];\n'
        # set node locations
        node_count = len(self.synteny_edges) * 2
        radius = node_count ** 1/4
        node_locations = [(cos(2 * pi / node_count * x) * radius, sin(2 * pi / node_count * x) * radius) for x in range(0, node_count + 1)]
        g += f'TERM [pos="0,0!"];\n'
        for s in self.synteny_edges:
            n1 = s.n1
            n2 = s.n2
            x1, y1 = node_locations.pop()
            x2, y2 = node_locations.pop()
            g += f'_{n1.id}_{n1.end.value}_ [pos="{x1},{y1}!"];\n'
            g += f'_{n2.id}_{n2.end.value}_ [pos="{x2},{y2}!"];\n'
        # set black edges representing synteny blocks
        for s in self.synteny_edges:
            n1 = s.n1
            n2 = s.n2
            g += f'_{n1.id}_{n1.end.value}_ -- _{n2.id}_{n2.end.value}_ [style=dashed, dir=forward];\n'
        # set blue edges (destination)
        for e in self.blue_edges.edges():
            label1 = 'TERM' if isinstance(e.n1, TerminalNode) else f'_{e.n1.id}_{e.n1.end.value}_'
            label2 = 'TERM' if isinstance(e.n2, TerminalNode) else f'_{e.n2.id}_{e.n2.end.value}_'
            g += f'{label1} -- {label2} [color=blue];\n'
        # draw red edges (source)
        for e in self.red_edges.edges():
            label1 = 'TERM' if isinstance(e.n1, TerminalNode) else f'_{e.n1.id}_{e.n1.end.value}_'
            label2 = 'TERM' if isinstance(e.n2, TerminalNode) else f'_{e.n2.id}_{e.n2.end.value}_'
            g += f'{label1} -- {label2} [color=red];\n'
        g += '}'
        return g


if __name__ == '__main__':
    bg = BreakpointGraph(
        # [['+A', '-B', '-D', '+C']],
        # [['+A', '+B', '+C', '+D']]
        [['+A', '+B'], ['-D', '-C'], ['-E']],
        [['+A', '-B', '-C', '+D'], ['+E']]
    )
    while (next_blue_edge := bg.find_blue_edge_in_non_trivial_path()) is not None:
        print(f'{bg.get_red_permutations()}')
        print(f'{bg.get_blue_permutations()}')
        print(f'{bg.get_red_blue_paths()}')
        print(f'{bg.to_neato_graph()}')
        bg.apply_2break(next_blue_edge)
    print(f'{bg.get_red_permutations()}')
    print(f'{bg.get_blue_permutations()}')
    print(f'{bg.get_red_blue_paths()}')
    print(f'{bg.to_neato_graph()}')