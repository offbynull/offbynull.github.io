from __future__ import annotations
from enum import Enum
from math import cos, pi, sin
from typing import List, Dict, Tuple, Optional, Set

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
    def __init__(self, id: Optional[str], end: SyntenyEnd):
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
        if isinstance(other, Node):
            return self.id == other.id and self.end == other.end
        else:
            return False

    def __hash__(self):
        return hash((self.id, self.end))

    def __str__(self):
        return str((self.id, self.end))

    def __repr__(self):
        return str(self)


class ColoredEdge:
    def __init__(self, n1: Optional[Node], n2: Optional[Node]):
        assert n1 != n2
        if n1 and n2:
            x = [n1, n2]
            x.sort()
            n1: Optional[Node] = x[0]
            n2: Optional[Node] = x[1]
        elif not n1 and not n2:
            raise ValueError('At least one must be not None')
        self.n1: Optional[Node] = n1
        self.n2: Optional[Node] = n2

    def get_other_node(self, nid: Optional[Node]):
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
        synteny_id_to_perm = {}
        synteny_id_to_edge = {}
        synteny_edges = []
        for p_num, p in enumerate(blue_p_list):
            for s in p:
                e, id = SyntenyEdge.from_str(s)
                synteny_edges.append(e)
                synteny_id_to_edge[id] = e
                synteny_id_to_perm[id] = p_num
        self.synteny_edges = synteny_edges
        self.synteny_id_to_edge = synteny_id_to_edge
        self.synteny_id_to_perm = synteny_id_to_perm

        self.node_to_blue_edges = BreakpointGraph._p_list_to_nodes(blue_p_list, synteny_id_to_perm)
        self.node_to_red_edges = BreakpointGraph._p_list_to_nodes(red_p_list, synteny_id_to_perm)

    @staticmethod
    def _p_list_to_nodes(p_list: List[List[str]], synteny_id_to_perm: Dict[str, int]):
        node_to_edges = {}
        for p in p_list:
            for (s1, s2), idx in slide_window(p, 2):
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
                node_to_edges[n1] = e
                node_to_edges[n2] = e
            # add link to dummy head
            p_head, p_head_id = SyntenyEdge.from_str(p[0])
            e = ColoredEdge(
                None,
                p_head.n1
            )
            node_to_edges[p_head.n1] = e
            # add link to dummy tail
            p_tail, p_tail_id = SyntenyEdge.from_str(p[-1])
            e = ColoredEdge(
                p_tail.n2,
                None
            )
            node_to_edges[p_tail.n2] = e
        return node_to_edges

    def _walk_red_blue(self, next_nid: Node, color: str, walked_nids: Set[Node]):
        path = []
        while True:
            if color == 'blue':
                edge = self.node_to_blue_edges[next_nid]
                color = 'red'
            elif color == 'red':
                edge = self.node_to_red_edges[next_nid]
                color = 'blue'
            else:
                raise ValueError('???')
            path.append(next_nid)
            walked_nids.add(next_nid)
            next_nid = edge.get_other_node(next_nid)
            if next_nid is None:  # reached terminus (end of chromosome), flip and try going in other direction
                break
            if next_nid in walked_nids:  # reached loop
                break
        return path

    def get_red_blue_paths(self):
        remaining_nids = set(self.node_to_blue_edges.keys())
        paths = []
        while remaining_nids:
            orig_nid = remaining_nids.pop()
            walked_nids = set()
            from_blue = self._walk_red_blue(orig_nid, 'blue', walked_nids)
            from_red = self._walk_red_blue(orig_nid, 'red', walked_nids)
            remaining_nids.difference_update(walked_nids)
            # both from_blue and from_red will start with orig_id, so clip if off one of them (from_red in this case)
            # and reverse the other before concatenating
            path = from_blue[::-1] + from_red[1:]
            paths += [path]
        return paths

    def find_blue_edge_in_non_trivial_cycle(self):
        for p in self.get_red_blue_paths():
            if len(p) == 1:
                continue
            if len(p) == 2 and self.node_to_red_edges[p[0]] == self.node_to_red_edges[p[1]]:
                continue
            return p
        return None

    def apply_2break(self, blue_edge: ColoredEdge):
        red_edge_1 = self.node_to_red_edges[blue_edge.n1]
        red_edge_2 = self.node_to_red_edges[blue_edge.n2]
        if blue_edge == red_edge_1 == red_edge_2:
            raise ValueError('Already in trivial cycle')
        nid1 = blue_edge.n1
        nid2 = red_edge_1.get_other_node(blue_edge.n1)
        nid3 = blue_edge.n2
        nid4 = red_edge_2.get_other_node(blue_edge.n2)
        # remove
        if nid1:
            del self.node_to_red_edges[nid1]
        if nid2:
            del self.node_to_red_edges[nid2]
        if nid3:
            del self.node_to_red_edges[nid3]
        if nid4:
            del self.node_to_red_edges[nid4]
        # re-wire
        if nid1:
            self.node_to_red_edges[nid1] = ColoredEdge(nid1, nid3)
        if nid3:
            self.node_to_red_edges[nid3] = ColoredEdge(nid1, nid3)
        if nid2:
            self.node_to_red_edges[nid2] = ColoredEdge(nid2, nid4)
        if nid4:
            self.node_to_red_edges[nid4] = ColoredEdge(nid2, nid4)

    def get_blue_permutations(self) -> List[List[str]]:
        return self._walk_to_permutations(self.node_to_blue_edges)

    def get_red_permutations(self) -> List[List[str]]:
        return self._walk_to_permutations(self.node_to_red_edges)

    def _walk_to_permutations(self, colored_edges: Dict[Node, ColoredEdge]) -> List[List[str]]:
        term_edges = set()
        for nid, ce in colored_edges.items():
            if ce.n1 is None or ce.n2 is None:
                term_edges.add(ce)
        perms = []
        while term_edges:
            ce = term_edges.pop()
            perm = []
            nid = ce.get_other_node(None)
            while nid:
                if nid.end == SyntenyEnd.TAIL:
                    perm.append('-' + nid.id)
                elif nid.end == SyntenyEnd.HEAD:
                    perm.append('+' + nid.id)
                else:
                    raise ValueError('???')
                nid = nid.other_end()
                ce = colored_edges[nid]
                nid = ce.get_other_node(nid)
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
        for e in set(self.node_to_blue_edges.values()):
            label1 = 'TERM' if e.n1 is None else f'_{e.n1.id}_{e.n1.end.value}_'
            label2 = 'TERM' if e.n2 is None else f'_{e.n2.id}_{e.n2.end.value}_'
            g += f'{label1} -- {label2} [color=blue];\n'
        # draw red edges (source)
        for e in set(self.node_to_red_edges.values()):
            label1 = 'TERM' if e.n1 is None else f'_{e.n1.id}_{e.n1.end.value}_'
            label2 = 'TERM' if e.n2 is None else f'_{e.n2.id}_{e.n2.end.value}_'
            g += f'{label1} -- {label2} [color=red];\n'
        g += '}'
        return g


if __name__ == '__main__':
    bg = BreakpointGraph(
        [['+A', '+B'], ['-D', '-C'], ['-E']],
        [['+A', '-B', '-C', '+D'], ['+E']]
    )
    while (next_path_to_break := bg.find_blue_edge_in_non_trivial_cycle()) is not None:
        print(f'{bg.get_red_permutations()}')
        print(f'{bg.get_blue_permutations()}')
        print(f'{bg.get_red_blue_paths()}')
        print(f'{bg.to_neato_graph()}')
        nid = next_path_to_break[0]
        edge = bg.node_to_blue_edges[nid]
        bg.apply_2break(edge)
    print(f'{bg.get_red_permutations()}')
    print(f'{bg.get_blue_permutations()}')
    print(f'{bg.get_red_blue_paths()}')
    print(f'{bg.to_neato_graph()}')