from __future__ import annotations

import textwrap
from math import cos, pi, sin
from typing import List

from breakpoint_graph.ColoredEdge import ColoredEdge
from breakpoint_graph.ColoredEdgeSet import ColoredEdgeSet
from breakpoint_graph.Permutation import Permutation
from breakpoint_graph.SyntenyEdge import SyntenyEdge
from breakpoint_graph.SyntenyEnd import SyntenyEnd
from breakpoint_graph.SyntenyNode import SyntenyNode
from breakpoint_graph.TerminalNode import TerminalNode


# This is similarto CyclicBreakpointGraph, except that it's assumed that the chromosomes aren't cyclic. That is, the
# chromosomes end at termination points rather than looping back in on themselves. The Pevzner book didn't document how
# to extend the cyclic chromosome algorithm to linear chromosome, so I made a set of assumptions here. I'm reasonably
# sure they're correct (the book said it's straight-forward to extend the algorithm to linear chromosomes).
from helpers.InputUtils import str_to_list


class BreakpointGraph:
    def __init__(self, red_p_list: List[List[str]], blue_p_list: List[List[str]]):
        self.blue_edges = ColoredEdgeSet.create(
            ce for p in blue_p_list for ce in Permutation.from_raw(p, False).to_colored_edges()
        )
        self.red_edges = ColoredEdgeSet.create(
            ce for p in red_p_list for ce in Permutation.from_raw(p, False).to_colored_edges()
        )

    def get_red_blue_paths(self) -> List[List[SyntenyNode]]:
        remaining_n_set = self.blue_edges.nodes()
        paths = []
        while remaining_n_set:
            orig_n = remaining_n_set.pop()
            walked_n_set = set()
            path_from_blue = ColoredEdgeSet.alternating_walk(orig_n, 0, [self.blue_edges, self.red_edges], walked_n_set)
            path_from_red = ColoredEdgeSet.alternating_walk(orig_n, 0, [self.blue_edges, self.red_edges], walked_n_set)
            # both path_from_blue and path_from_red will start with orig_id, so clip if off one of them (from_red in
            # this case) and reverse the other before concatenating
            path = path_from_blue[::-1] + path_from_red[1:]
            paths += [path]
            remaining_n_set.difference_update(walked_n_set)
        return paths

    def find_blue_edge_in_non_trivial_path(self):
        for p in self.get_red_blue_paths():
            if len(p) == 1:
                continue
            if len(p) == 2 and self.red_edges.find(p[0]) == self.red_edges.find(p[1]):
                continue
            return self.blue_edges.find(p[0])
        return None

    def two_break(self, blue_edge: ColoredEdge):
        red_edge1 = self.red_edges.remove(blue_edge.n1)  # If blue_edge.n1 is TERM, will return None
        red_edge2 = self.red_edges.remove(blue_edge.n2)  # If blue_edge.n2 is TERM, will return None
        # Given that you want one of the new red_edges to match blue_edge, this will return the OTHER new red edge. That
        # is, it'll swap the ends of the existing red edges such that one of the new red_edges is blue_edge and the
        # other new red_edge gets returned.
        new_red_edge = ColoredEdge.swap_ends(red_edge1, red_edge2, blue_edge)
        self.red_edges.insert(blue_edge)
        if new_red_edge:  # It's possible both ends for new_red_edge were TERM, in which case it'll be None
            self.red_edges.insert(new_red_edge)

    # IIRC, the 2 break distance is the minimum number of 2 breaks required to get red edges == blue edges. Section 6.18
    # of The Pevzner book claims that this is hard set to Blocks(P, Q)− Cycles(P, Q) + 1:
    #     However, the lower bound drev(P, Q) ≥ Blocks(P, Q) + 1 − Cycles(P, Q) approximates the reversal distance
    #     between linear permutations extremely well. This intriguing performance raised the question of whether this
    #     bound is close to an exact formula. In 1999, Hannenhalli and Pevzner found this formula by defining two
    #     special types of breakpoint graph structures called “hurdles” and “fortresses”. Denoting the number of hurdles
    #     and fortresses in BreakpointGraph(P, Q) by Hurdles(P, Q)and Fortresses(P, Q), respectively, they proved that
    #     the reversal distance is given by
    #         drev(P, Q) = Blocks(P, Q) + 1 − Cycles(P, Q) + Hurdles(P, Q) + Fortresses(P, Q).
    #     Using this formula, they developed a polynomial algorithm for computing drev(P, Q). Nevertheless,
    #     Hurdles(P, Q) and Fortresses(P, Q) are small for the vast majority of permutations, and so the lower bound
    #     Blocks(P, Q) + 1 − Cycles(P, Q) is a good approximation of the reversal distance in practice.
    # I have access to the original paper that describes the full algorithm in detail but I haven't had time to go
    # through it.
    def two_break_distance(self):
        red_blue_path_cnt = len(self.get_red_blue_paths())
        synteny_block_cnt = len([e for e in self.blue_edges.walk() if isinstance(e, SyntenyEdge)])
        return synteny_block_cnt + 1 - red_blue_path_cnt

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
        g += f'TERM [pos="0,0!"];\n'
        for s in syn_edges:
            n1 = s.n1
            n2 = s.n2
            x1, y1 = node_locations.pop()
            x2, y2 = node_locations.pop()
            g += f'_{n1.id}_{n1.end.value}_ [pos="{x1},{y1}!"];\n'
            g += f'_{n2.id}_{n2.end.value}_ [pos="{x2},{y2}!"];\n'
        # set black edges representing synteny blocks
        for s in syn_edges:
            dir = 'forward' if n1.end == SyntenyEnd.HEAD else 'back'
            g += f'_{n1.id}_{n1.end.value}_ -- _{n2.id}_{n2.end.value}_ [style=dashed, dir={dir}];\n'
        # set blue edges (destination)
        for e in blue_edges:
            label1 = 'TERM' if isinstance(e.n1, TerminalNode) else f'_{e.n1.id}_{e.n1.end.value}_'
            label2 = 'TERM' if isinstance(e.n2, TerminalNode) else f'_{e.n2.id}_{e.n2.end.value}_'
            g += f'{label1} -- {label2} [color=blue];\n'
        # draw red edges (source)
        for e in red_edges:
            label1 = 'TERM' if isinstance(e.n1, TerminalNode) else f'_{e.n1.id}_{e.n1.end.value}_'
            label2 = 'TERM' if isinstance(e.n2, TerminalNode) else f'_{e.n2.id}_{e.n2.end.value}_'
            g += f'{label1} -- {label2} [color=red];\n'
        g += '}'
        return g


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        red_p_list, _ = str_to_list(input().strip(), 0)
        blue_p_list, _ = str_to_list(input().strip(), 0)
        show_graph_str = input().strip()
        if show_graph_str == 'graph_show':
            show_graph = True
        elif show_graph_str == 'graph_hide':
            show_graph = False
        else:
            raise ValueError(f'{show_graph_str=} must be entire graph_show or graph_hide')
        print(f'Applying 2-breaks on circular genome until {red_p_list=} matches {blue_p_list=} ({show_graph=})...\n')
        bg = BreakpointGraph(red_p_list, blue_p_list)
        while (next_blue_edge := bg.find_blue_edge_in_non_trivial_path()) is not None:
            bg.two_break(next_blue_edge)
            red_p_list = bg.get_red_permutations()
            print(f' * {red_p_list=}')
            if show_graph:
                print(f'')
                print(f'   ```{{dot}}')
                print(f'{textwrap.indent(bg.to_neato_graph(), "   ")}')
                print(f'   ```')
        print('\n')
        print(
            f'Recall that the the breakpoint graph is undirected. A permutation may have been walked in either'
            f' direction (clockwise vs counter-clockwise) and there are multiple nodes to start walking from. If the'
            f' output looks like it\'s going backwards, that\'s just as correct as if it looked like it\'s going'
            f' forward.\n'
            f'\n'
            f'Also, recall that a genome is represented as a set of permutations -- sets are not ordered.')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()
    # bg = BreakpointGraph(
    #     # [['+A', '+B', '+C', '-F', '-E', '-D']],
    #     # [['+A', '+B', '+C', '+D', '+E', '+F']]
    #     [['+F', '+E', '+D']],
    #     [['+D', '+E', '+F']]
    #     # [['+A', '+B'], ['-D', '-C'], ['-E']],
    #     # [['+A', '-B', '-C', '+D'], ['+E']]
    # )
    # while (next_blue_edge := bg.find_blue_edge_in_non_trivial_path()) is not None:
    #     print(f'{bg.get_red_permutations()}')
    #     print(f'{bg.get_blue_permutations()}')
    #     print(f'{bg.get_red_blue_paths()}')
    #     print(f'{bg.to_neato_graph()}')
    #     bg.two_break(next_blue_edge)
    # print(f'{bg.get_red_permutations()}')
    # print(f'{bg.get_blue_permutations()}')
    # print(f'{bg.get_red_blue_paths()}')
    # print(f'{bg.to_neato_graph()}')