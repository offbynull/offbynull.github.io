from __future__ import annotations

from enum import Enum
from typing import List

from helpers.Utils import slide_window
from synteny_graph.GeometryUtils import distance


class MatchType(Enum):
    NORMAL = 'NORMAL',
    REVERSE_COMPLEMENT = 'REVERSE_COMPLEMENT'


class Match:
    __slots__ = ['y_axis_chromosome', 'y_axis_chromosome_min_idx', 'y_axis_chromosome_max_idx',
                 'x_axis_chromosome', 'x_axis_chromosome_min_idx', 'x_axis_chromosome_max_idx', 'type']

    def __init__(
            self,
            y_axis_chromosome: str,
            y_axis_chromosome_min_idx: int,
            y_axis_chromosome_max_idx: int,
            x_axis_chromosome: str,
            x_axis_chromosome_min_idx: int,
            x_axis_chromosome_max_idx: int,
            type: MatchType):
        assert x_axis_chromosome_min_idx < x_axis_chromosome_max_idx
        assert y_axis_chromosome_min_idx < y_axis_chromosome_max_idx
        self.y_axis_chromosome = y_axis_chromosome
        self.y_axis_chromosome_min_idx = y_axis_chromosome_min_idx
        self.y_axis_chromosome_max_idx = y_axis_chromosome_max_idx
        self.x_axis_chromosome = x_axis_chromosome
        self.x_axis_chromosome_min_idx = x_axis_chromosome_min_idx
        self.x_axis_chromosome_max_idx = x_axis_chromosome_max_idx
        self.type = type

    @staticmethod
    def merge(forward_chain: List[Match]):
        assert forward_chain, 'Empty chain'
        assert all(forward_chain[0].y_axis_chromosome == m.y_axis_chromosome
                   and forward_chain[0].x_axis_chromosome == m.x_axis_chromosome
                   and forward_chain[0].type == m.type
                   for m in forward_chain), 'Chain type and/or chromosome mismatch'
        if len(forward_chain) > 2:
            assert all(a.x_axis_chromosome_max_idx <= b.x_axis_chromosome_min_idx
                       for (a, b), _ in slide_window(forward_chain, 2)), 'Chain not ordered'
        y_axis_chromosome = forward_chain[0].y_axis_chromosome
        x_axis_chromosome = forward_chain[0].x_axis_chromosome
        x_axis_chromosome_min_idx = forward_chain[0].x_axis_chromosome_min_idx
        x_axis_chromosome_max_idx = forward_chain[-1].x_axis_chromosome_max_idx
        type = forward_chain[0].type
        if type == MatchType.NORMAL:
            y_axis_chromosome_min_idx = forward_chain[0].y_axis_chromosome_min_idx
            y_axis_chromosome_max_idx = forward_chain[-1].y_axis_chromosome_max_idx
        elif type == MatchType.REVERSE_COMPLEMENT:
            y_axis_chromosome_min_idx = forward_chain[-1].y_axis_chromosome_min_idx
            y_axis_chromosome_max_idx = forward_chain[0].y_axis_chromosome_max_idx
        else:
            raise ValueError('???')
        new_m = Match(
            y_axis_chromosome,
            y_axis_chromosome_min_idx,
            y_axis_chromosome_max_idx,
            x_axis_chromosome,
            x_axis_chromosome_min_idx,
            x_axis_chromosome_max_idx,
            type
        )
        return new_m

    def get_start_point(self):
        if self.type == MatchType.NORMAL:
            return self.x_axis_chromosome_min_idx, self.y_axis_chromosome_min_idx
        elif self.type == MatchType.REVERSE_COMPLEMENT:
            return self.x_axis_chromosome_min_idx, self.y_axis_chromosome_max_idx
        else:
            raise ValueError('???')

    def get_end_point(self):
        if self.type == MatchType.NORMAL:
            return self.x_axis_chromosome_max_idx, self.y_axis_chromosome_max_idx
        elif self.type == MatchType.REVERSE_COMPLEMENT:
            return self.x_axis_chromosome_max_idx, self.y_axis_chromosome_min_idx
        else:
            raise ValueError('???')

    def get_length(self):
        start_pt = self.get_start_point()
        end_pt = self.get_end_point()
        return distance(end_pt[0], start_pt[0], end_pt[1], start_pt[1])