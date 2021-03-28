from enum import Enum
from typing import Iterable


class MatchType(Enum):
    NORMAL = 'NORMAL',
    REVERSE_COMPLEMENT = 'REVERSE_COMPLEMENT'


class Match:
    __slots__ = ['src_chromosome', 'src_start_idx', 'src_end_idx', 'dst_chromosome', 'dst_start_idx', 'dst_end_idx',
                 'match_type']

    def __init__(
            self,
            src_chromosome: str,
            src_start_idx: int,
            src_end_idx: int,
            dst_chromosome: str,
            dst_start_idx: int,
            dst_end_idx: int,
            match_type: MatchType):
        self.src_chromosome = src_chromosome
        self.src_start_idx = src_start_idx
        self.src_end_idx = src_end_idx
        self.dst_chromosome = dst_chromosome
        self.dst_start_idx = dst_start_idx
        self.dst_end_idx = dst_end_idx
        self.match_type = match_type


class SyntenyGraph:
    def __init__(self, matches: Iterable[Match]):
        ...