from __future__ import annotations

from enum import Enum
from typing import List


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


class Permutation:
    def __init__(self, blocks: List[Block], cyclic: bool):
        if cyclic:
            v = min(blocks)
            i = blocks.index(v)
            blocks = blocks[i:] + blocks[:i]
        self.blocks = blocks
        self.cyclic = cyclic

    def _flip(self):
        return Permutation([Block(x.dir.flip(), x.id) for x in reversed(self.blocks)], self.cyclic)

    def __eq__(self, other: Permutation):
        return (self.blocks == other.blocks or self.blocks == other._flip().blocks) and self.cyclic == other.cyclic

    def to_raw(self) -> List[str]:
        return [str(s) for s in self.blocks]

    @staticmethod
    def from_raw(l: List[str], cyclic: bool) -> Permutation:
        assert len(l) > 0
        blocks = []
        for v in l:
            b = Block.from_str(v)
            blocks.append(b)
        return Permutation(blocks, cyclic)


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

    p1 = Permutation.from_raw(['+A', '+B', '+C'], False)
    p2 = Permutation.from_raw(['-C', '-B', '-A'], False)  # flipped
    print(f'{p1.to_raw()}')
    print(f'{p2.to_raw()}')