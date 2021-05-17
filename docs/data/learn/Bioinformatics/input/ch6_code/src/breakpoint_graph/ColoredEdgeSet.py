from __future__ import annotations

from typing import Optional, Dict, Set, Union, Iterable, List

from BreakpointGraph import SyntenyEnd
from breakpoint_graph.ColoredEdge import ColoredEdge
from breakpoint_graph.SyntenyEdge import SyntenyEdge
from breakpoint_graph.SyntenyNode import SyntenyNode
from breakpoint_graph.TerminalNode import TerminalNode

from helpers.Utils import slide_window


# MARKDOWN
# Represents a single genome in a breakpoint graph
class ColoredEdgeSet:
    def __init__(self):
        self.by_node: Dict[SyntenyNode, ColoredEdge] = {}

    @staticmethod
    def create(ce_list: Iterable[ColoredEdge]) -> ColoredEdgeSet:
        ret = ColoredEdgeSet()
        for ce in ce_list:
            ret.insert(ce)
        return ret

    def insert(self, e: ColoredEdge):
        if e.n1 in self.by_node or e.n2 in self.by_node:
            raise ValueError(f'Node already occupied: {e}')
        if not isinstance(e.n1, TerminalNode):
            self.by_node[e.n1] = e
        if not isinstance(e.n2, TerminalNode):
            self.by_node[e.n2] = e
# MARKDOWN

    def find(self, n: Union[SyntenyNode, TerminalNode]) -> Optional[ColoredEdge]:
        return self.by_node.get(n, None)

    def find_all(self, *n: Union[SyntenyNode, TerminalNode]) -> Set[ColoredEdge]:
        ret = set()
        for _n in n:
            found = self.find(_n)
            if found is not None:
                ret.add(found)
        return ret

    def remove(self, n: Union[SyntenyNode, TerminalNode]) -> Optional[ColoredEdge]:
        if n == TerminalNode.INST:  # terminal nodes are not tracked -- always returns none
            return None
        e = self.by_node.pop(n, None)
        if e is None:
            return None
        n = e.other_end(n)
        if n != TerminalNode.INST:
            self.by_node.pop(n)
        return e

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

# WALK_MARKDOWN
    # Walks the colored edges, spliced with synteny edges.
    def walk(self) -> List[List[Union[ColoredEdge, SyntenyEdge]]]:
        ret = []
        all_edges = self.edges()
        term_edges = set()
        for ce in all_edges:
            if ce.has_term():
                term_edges.add(ce)
        # handle linear chromosomes
        while term_edges:
            ce = term_edges.pop()
            n = ce.non_term()
            all_edges.remove(ce)
            edges = []
            while True:
                se_n1 = n
                se_n2 = se_n1.swap_end()
                se = SyntenyEdge(se_n1, se_n2)
                edges += [ce, se]
                ce = self.by_node[se_n2]
                if ce.has_term():
                    edges += [ce]
                    term_edges.remove(ce)
                    all_edges.remove(ce)
                    break
                n = ce.other_end(se_n2)
                all_edges.remove(ce)
            ret.append(edges)
        # handle cyclic chromosomes
        while all_edges:
            start_ce = all_edges.pop()
            ce = start_ce
            n = ce.n1
            edges = []
            while True:
                se_n1 = n
                se_n2 = se_n1.swap_end()
                se = SyntenyEdge(se_n1, se_n2)
                edges += [ce, se]
                ce = self.by_node[se_n2]
                if ce == start_ce:
                    break
                n = ce.other_end(se_n2)
                all_edges.remove(ce)
            ret.append(edges)
        return ret
# WALK_MARKDOWN

    # Use this to walk red-blue cycles
    @staticmethod
    def alternating_walk(
            next_n: SyntenyNode,
            next_ce_idx: int,
            ce_sets: List[ColoredEdgeSet],
            walked_n_set: Set[SyntenyNode]
    ) -> List[SyntenyNode]:
        path = []
        while True:
            ce_set = ce_sets[next_ce_idx]
            ce = ce_set.find(next_n)
            path.append(next_n)
            walked_n_set.add(next_n)
            next_n = ce.other_end(next_n)
            next_ce_idx = (next_ce_idx + 1) % len(ce_sets)  # rotate to next ce_set
            if next_n == TerminalNode.INST:  # reached terminus (termination condition for linear chromosomes)
                break
            if next_n in walked_n_set:  # reached loop (termination condition for cyclic chromosomes)
                break
        return path

    def __str__(self):
        return str(set(self.by_node.values()))

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash(frozenset(self.by_node.values()))


def main_walk():
    ce_set = ColoredEdgeSet()
    lookup = {
        '+': SyntenyEnd.HEAD,
        '-': SyntenyEnd.HEAD
    }
    vals = [s.strip() for s in input().strip().split(',')]
    print(f'Given the permutation {vals}...\n')
    cyclic = vals[0] != ''
    for (s1, s2), _ in slide_window(vals, 2, cyclic=cyclic):
        if s1 == '':
            s1_node = TerminalNode.INST
        else:
            s1_node = SyntenyNode(
                id=s1[1:],
                end=lookup[s1[0]]
            )
        if s2 == '':
            s2_node = TerminalNode.INST
        else:
            s2_node = SyntenyNode(
                id=s2[1:],
                end=lookup[s2[0]].swap()
            )
        ce = ColoredEdge(s1_node, s2_node)
        ce_set.insert(ce)
    for chromosome in ce_set.walk():
        print(f' * START')
        for edge in chromosome:
            print(f'   * {edge}')
    print('')
    print(f'CE means colored edge / SE means synteny edge.\n')
    print(f'Recall that the the breakpoint graph is undirected / a permutation may have been walked in either direction'
          f'(clockwise vs counter-clockwise). If the output looks like it\'s going backwards, that\'s just as correct'
          f' as if it looked like it\'s going forward.')


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        func_name = input().strip()
        if func_name == 'walk':
            main_walk()
        else:
            raise ValueError(f'Unrecognized {func_name=}')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()
# if __name__ == '__main__':
#     l = ColoredEdgeSet.create([
#         ColoredEdge(SyntenyNode('A', SyntenyEnd.TAIL), SyntenyNode('B', SyntenyEnd.HEAD)),
#         ColoredEdge(SyntenyNode('B', SyntenyEnd.TAIL), SyntenyNode('C', SyntenyEnd.HEAD)),
#         ColoredEdge(SyntenyNode('C', SyntenyEnd.TAIL), SyntenyNode('A', SyntenyEnd.HEAD)),
#         ColoredEdge(TerminalNode.INST, SyntenyNode('X', SyntenyEnd.HEAD)),
#         ColoredEdge(SyntenyNode('X', SyntenyEnd.TAIL), SyntenyNode('Y', SyntenyEnd.HEAD)),
#         ColoredEdge(SyntenyNode('Y', SyntenyEnd.TAIL), SyntenyNode('Z', SyntenyEnd.HEAD)),
#         ColoredEdge(SyntenyNode('Z', SyntenyEnd.TAIL), TerminalNode.INST),
#     ]).walk()
#     print(f'{l}')
