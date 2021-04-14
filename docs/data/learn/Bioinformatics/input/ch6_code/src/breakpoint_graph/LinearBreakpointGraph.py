from __future__ import annotations

from math import cos, pi, sin
from typing import List, Dict, Set, Union

from breakpoint_graph.ColoredEdge import ColoredEdge
from breakpoint_graph.ColoredEdgeSet import ColoredEdgeSet
from breakpoint_graph.SyntenyNode import SyntenyNode
from breakpoint_graph.SyntenyEdge import SyntenyEdge
from breakpoint_graph.SyntenyEnd import SyntenyEnd
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
            for (s1, s2), idx in slide_window(p, 2):
                if s1[0] == '-' and s2[0] == '+':
                    n1 = SyntenyNode(s1[1:], SyntenyEnd.HEAD)
                    n2 = SyntenyNode(s2[1:], SyntenyEnd.HEAD)
                elif s1[0] == '+' and s2[0] == '-':
                    n1 = SyntenyNode(s1[1:], SyntenyEnd.TAIL)
                    n2 = SyntenyNode(s2[1:], SyntenyEnd.TAIL)
                elif s1[0] == '+' and s2[0] == '+':
                    n1 = SyntenyNode(s1[1:], SyntenyEnd.TAIL)
                    n2 = SyntenyNode(s2[1:], SyntenyEnd.HEAD)
                elif s1[0] == '-' and s2[0] == '-':
                    n1 = SyntenyNode(s1[1:], SyntenyEnd.HEAD)
                    n2 = SyntenyNode(s2[1:], SyntenyEnd.TAIL)
                else:
                    raise ValueError('???')
                ret.insert(
                    ColoredEdge(n1, n2)
                )
            # add link to dummy head
            p_head, p_head_id = SyntenyEdge.from_str(p[0])
            ret.insert(
                ColoredEdge(TerminalNode.INST, p_head.n1)
            )
            # add link to dummy tail
            p_tail, p_tail_id = SyntenyEdge.from_str(p[-1])
            ret.insert(
                ColoredEdge(p_tail.n2, TerminalNode.INST)
            )
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
            if isinstance(next_n, TerminalNode):  # reached terminus (end of chromosome), flip and try going in other direction
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
        if blue_edge.has_term_node():
            n = blue_edge.other_end(TerminalNode.INST)
            red_edge1 = self.red_edges.find(n)
            if blue_edge == red_edge1:
                raise ValueError('Already in trivial cycle')
            self.red_edges.insert(
                ColoredEdge(n, red_edge1.other_end(n))
            )
        else:
            red_edge1 = self.red_edges.find(blue_edge.n1)
            red_edge2 = self.red_edges.find(blue_edge.n2)
            if blue_edge == red_edge1 == red_edge2:
                raise ValueError('Already in trivial cycle')
            self.red_edges.remove_edge(red_edge1)
            self.red_edges.remove_edge(red_edge2)
            self.red_edges.insert(
                ColoredEdge(
                    blue_edge.n1,
                    blue_edge.n2
                )
            )
            if {red_edge1.other_end(blue_edge.n1), red_edge2.other_end(blue_edge.n2)} != {TerminalNode.INST}:
                self.red_edges.insert(
                    ColoredEdge(
                        red_edge1.other_end(blue_edge.n1),
                        red_edge2.other_end(blue_edge.n2)
                    )
                )

    def get_blue_permutations(self) -> List[List[str]]:
        return self._walk_to_permutations(self.blue_edges)

    def get_red_permutations(self) -> List[List[str]]:
        return self._walk_to_permutations(self.red_edges)

    def _walk_to_permutations(self, colored_edges: ColoredEdgeSet) -> List[List[str]]:
        term_edges = set()
        for ce in colored_edges.edges():
            if ce.has_term_node():
                term_edges.add(ce)
        perms = []
        while term_edges:
            ce = term_edges.pop()
            perm = []
            n = ce.other_end(TerminalNode.INST)
            while not isinstance(n, TerminalNode):
                if n.end == SyntenyEnd.TAIL:
                    perm.append('-' + n.id)
                elif n.end == SyntenyEnd.HEAD:
                    perm.append('+' + n.id)
                else:
                    raise ValueError('???')
                n = n.other_end()
                ce = colored_edges.find(n)
                n = ce.other_end(n)
            term_edges.remove(ce)  # remove other end of chain (eventually it'll go back into None / TERM)
            perms.append(perm)
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
        # print(f'{bg.get_blue_permutations()}')
        # print(f'{bg.get_red_blue_paths()}')
        # print(f'{bg.to_neato_graph()}')
        bg.apply_2break(next_blue_edge)
    print(f'{bg.get_red_permutations()}')
    # print(f'{bg.get_blue_permutations()}')
    # print(f'{bg.get_red_blue_paths()}')
    # print(f'{bg.to_neato_graph()}')