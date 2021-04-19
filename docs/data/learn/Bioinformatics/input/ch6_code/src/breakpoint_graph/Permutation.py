from __future__ import annotations

from enum import Enum
from typing import List, Set, Tuple

from breakpoint_graph.ColoredEdge import ColoredEdge
from breakpoint_graph.ColoredEdgeSet import ColoredEdgeSet
from breakpoint_graph.SyntenyEdge import SyntenyEdge
from breakpoint_graph.SyntenyEnd import SyntenyEnd
from breakpoint_graph.SyntenyNode import SyntenyNode
from breakpoint_graph.TerminalNode import TerminalNode
from helpers.Utils import slide_window


class Direction(Enum):
    FORWARD = '+'
    BACKWARD = '-'

    def flip(self):
        if self == Direction.FORWARD:
            return Direction.BACKWARD
        elif self == Direction.BACKWARD:
            return Direction.FORWARD
        else:
            raise ValueError('???')

    def __lt__(self, other):
        a = 1 if self == Direction.FORWARD else 0
        b = 1 if other == Direction.FORWARD else 0
        return a < b


class Block:
    __slots__ = ['dir', 'id']

    def __init__(self, dir: Direction, id: str):
        self.dir = dir
        self.id = id

    def __lt__(self, other):
        return (self.dir, self.id) < (other.dir, other.id)

    def __eq__(self, other):
        return (self.dir, self.id) == (other.dir, other.id)

    def __str__(self):
        return self.dir.value + self.id

    def __repr__(self):
        return str(self)

    @staticmethod
    def from_str(v: str) -> Block:
        if v[0] == '+':
            return Block(Direction.FORWARD, v[1:])
        elif v[0] == '-':
            return Block(Direction.BACKWARD, v[1:])
        else:
            raise ValueError('???')

    def to_synteny_edge(self) -> SyntenyEdge:
        if self.dir == Direction.FORWARD:
            return SyntenyEdge(
                SyntenyNode(self.id, SyntenyEnd.HEAD),
                SyntenyNode(self.id, SyntenyEnd.TAIL)
            )
        elif self.dir == Direction.BACKWARD:
            return SyntenyEdge(
                SyntenyNode(self.id, SyntenyEnd.TAIL),
                SyntenyNode(self.id, SyntenyEnd.HEAD)
            )
        else:
            raise ValueError('???')


class Permutation:
    def __init__(self, blocks: List[Block], cyclic: bool):
        self.blocks = blocks
        self.cyclic = cyclic

    def _flip(self):
        return Permutation([Block(x.dir.flip(), x.id) for x in reversed(self.blocks)], self.cyclic)

    def __eq__(self, other: Permutation):
        return (self.blocks == other.blocks or self.blocks == other._flip().blocks) and self.cyclic == other.cyclic

    def to_raw(self) -> List[str]:
        return [str(s) for s in self.blocks]

    # Check if smallest block ID is negative, if so flip the permutation so that block ID becomes positive. Also, if the
    # permutation is cyclic, shift it so that it starts from that smallest block ID. These modifications make it so that
    # that regardless of which direction the original colored edges were walked in / which node the walk started from
    # (if it was cyclic), the output would be the same.
    def to_normalized_raw(self) -> List[str]:
        p = self
        min_b = min(p.blocks, key=lambda x: x.id)
        if min_b.dir == Direction.BACKWARD:
            p = p._flip()
        min_b = min(p.blocks, key=lambda x: x.id)
        if p.cyclic:
            i = p.blocks.index(min_b)
            blocks = p.blocks[i:] + p.blocks[:i]
        else:
            blocks = p.blocks
        return [str(s) for s in blocks]

    def to_colored_edges(self) -> List[ColoredEdge]:
        ret = []
        # add link to dummy head if linear
        if not self.cyclic:
            b = self.blocks[0]
            ret.append(
                ColoredEdge(TerminalNode.INST, b.to_synteny_edge().n1)
            )
        # add normal edges
        for (b1, b2), idx in slide_window(self.blocks, 2):
            if b1.dir == Direction.BACKWARD and b2.dir == Direction.FORWARD:
                n1 = SyntenyNode(b1.id, SyntenyEnd.HEAD)
                n2 = SyntenyNode(b2.id, SyntenyEnd.HEAD)
            elif b1.dir == Direction.FORWARD and b2.dir == Direction.BACKWARD:
                n1 = SyntenyNode(b1.id, SyntenyEnd.TAIL)
                n2 = SyntenyNode(b2.id, SyntenyEnd.TAIL)
            elif b1.dir == Direction.FORWARD and b2.dir == Direction.FORWARD:
                n1 = SyntenyNode(b1.id, SyntenyEnd.TAIL)
                n2 = SyntenyNode(b2.id, SyntenyEnd.HEAD)
            elif b1.dir == Direction.BACKWARD and b2.dir == Direction.BACKWARD:
                n1 = SyntenyNode(b1.id, SyntenyEnd.HEAD)
                n2 = SyntenyNode(b2.id, SyntenyEnd.TAIL)
            else:
                raise ValueError('???')
            ret.append(
                ColoredEdge(n1, n2)
            )
        # add link to dummy tail if linear
        if not self.cyclic:
            b = self.blocks[-1]
            ret.append(
                ColoredEdge(b.to_synteny_edge().n2, TerminalNode.INST)
            )
        # return
        return ret

    @staticmethod
    def from_raw(l: List[str], cyclic: bool) -> Permutation:
        assert len(l) > 0
        blocks = []
        for v in l:
            b = Block.from_str(v)
            blocks.append(b)
        return Permutation(blocks, cyclic)

    @staticmethod
    def from_colored_edges(
            colored_edges: ColoredEdgeSet,
            start_n: SyntenyNode,
            cyclic: bool
    ) -> Tuple[Permutation, Set[ColoredEdge]]:
        # if not cyclic, it's expected that start_n is either from or to a term node
        if not cyclic:
            ce = colored_edges.find(start_n)
            assert ce.has_term(), "Start node must be for a terminal colored edge"
        # if cyclic stop once you detect a loop, otherwise  stop once you encounter a term node
        if cyclic:
            walked = set()
            def stop_test(x):
                ret = x in walked
                walked.add(next_n)
                return ret
        else:
            def stop_test(x):
                return x == TerminalNode.INST
        # begin loop
        blocks = []
        start_ce = colored_edges.find(start_n)
        walked_ce_set = {start_ce}
        next_n = start_n
        while not stop_test(next_n):
            if next_n.end == SyntenyEnd.HEAD:
                b = Block(Direction.FORWARD, next_n.id)
            elif next_n.end == SyntenyEnd.TAIL:
                b = Block(Direction.BACKWARD, next_n.id)
            else:
                raise ValueError('???')
            blocks.append(b)
            swapped_n = next_n.swap_end()
            next_ce = colored_edges.find(swapped_n)
            next_n = next_ce.other_end(swapped_n)
            walked_ce_set.add(next_ce)
        return Permutation(blocks, cyclic), walked_ce_set


if __name__ == '__main__':
    p1 = Permutation.from_raw(['+A', '+B', '+C'], False)
    p2 = Permutation.from_raw(['+A', '+B', '+C'], False)  # same
    print(f'{p1 == p2}')
    p1 = Permutation.from_raw(['+A', '+B', '+C'], False)
    p2 = Permutation.from_raw(['-C', '-B', '-A'], False)  # flipped
    print(f'{p1 == p2}')
    p1 = Permutation.from_raw(['+A', '+B', '+C'], False)
    p2 = Permutation.from_raw(['+A', '+C', '+B'], False)  # out of order -- should fail
    print(f'{p1 == p2}')
    p1 = Permutation.from_raw(['+B', '+A', '+C'], True)
    p2 = Permutation.from_raw(['+B', '+A', '+C'], True)  # same
    print(f'{p1 == p2}')
    p1 = Permutation.from_raw(['+B', '+A', '+C'], True)
    p2 = Permutation.from_raw(['+A', '+C', '+B'], True)  # rotate left 1
    print(f'{p1 == p2}')
    p1 = Permutation.from_raw(['+B', '+A', '+C'], True)
    p2 = Permutation.from_raw(['+C', '+B', '+A'], True)  # rotate left 2
    print(f'{p1 == p2}')
    p1 = Permutation.from_raw(['+B', '+A', '+C'], True)
    p2 = Permutation.from_raw(['-C', '-A', '-B'], True)  # flipped
    print(f'{p1 == p2}')
    p1 = Permutation.from_raw(['+B', '+A', '+C'], True)
    p2 = Permutation.from_raw(['-A', '-B', '-C'], True)  # flipped + rotate left 1
    print(f'{p1 == p2}')
    p1 = Permutation.from_raw(['+B', '+A', '+C'], True)
    p2 = Permutation.from_raw(['-B', '-C', '-A'], True)  # flipped + rotate left 2
    print(f'{p1 == p2}')
    p1 = Permutation.from_raw(['+A', '+B', '+C'], True)
    p2 = Permutation.from_raw(['+A', '+C', '+B'], True)  # out of order -- should fail
    print(f'{p1 == p2}')
    p1 = Permutation.from_raw(['+A', '+B', '+C'], True)
    p2 = Permutation.from_raw(['-C', '-A', '-B'], True)  # flipped + out of order -- should fail
    print(f'{p1 == p2}')

    p1 = Permutation.from_raw(['+D', '+B', '+C'], False)
    p2 = Permutation.from_raw(['-C', '-B', '-D'], False)  # flipped
    print(f'{p1.to_raw()} / {p1.to_normalized_raw()}')
    print(f'{p2.to_raw()} / {p1.to_normalized_raw()}')

    ces = ColoredEdgeSet()
    ces.insert(ColoredEdge(TerminalNode.INST, SyntenyNode('A', SyntenyEnd.HEAD)))
    ces.insert(ColoredEdge(SyntenyNode('A', SyntenyEnd.TAIL), SyntenyNode('B', SyntenyEnd.TAIL)))
    ces.insert(ColoredEdge(SyntenyNode('B', SyntenyEnd.HEAD), TerminalNode.INST))
    p1, _ = Permutation.from_colored_edges(ces, SyntenyNode('B', SyntenyEnd.HEAD), False)
    p2, _ = Permutation.from_colored_edges(ces, SyntenyNode('A', SyntenyEnd.HEAD), False)
    print(f'{p1.to_raw()} / {p1.to_normalized_raw()}')
    print(f'{p2.to_raw()} / {p1.to_normalized_raw()}')
    print(f'{p1 == p2}')

    ces = ColoredEdgeSet()
    ces.insert(ColoredEdge(SyntenyNode('A', SyntenyEnd.HEAD), SyntenyNode('B', SyntenyEnd.HEAD)))
    ces.insert(ColoredEdge(SyntenyNode('B', SyntenyEnd.TAIL), SyntenyNode('C', SyntenyEnd.TAIL)))
    ces.insert(ColoredEdge(SyntenyNode('C', SyntenyEnd.HEAD), SyntenyNode('D', SyntenyEnd.HEAD)))
    ces.insert(ColoredEdge(SyntenyNode('D', SyntenyEnd.TAIL), SyntenyNode('A', SyntenyEnd.TAIL)))
    p1, _ = Permutation.from_colored_edges(ces, SyntenyNode('B', SyntenyEnd.HEAD), True)
    p2, _ = Permutation.from_colored_edges(ces, SyntenyNode('A', SyntenyEnd.HEAD), True)
    print(f'{p1.to_raw()} / {p1.to_normalized_raw()}')
    print(f'{p2.to_raw()} / {p1.to_normalized_raw()}')
    print(f'{p1 == p2}')
    print(f'{p1.to_colored_edges()}')
    print(f'{p2.to_colored_edges()}')