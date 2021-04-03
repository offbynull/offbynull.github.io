from __future__ import annotations

from bisect import bisect_left
from enum import Enum
from typing import List, Dict, Iterator, Set, Union

from synteny_graph.Match import Match, MatchType


class Axis(Enum):
    X = 'X',
    Y = 'Y'


class Overlap:
    def __init__(self, before: Span, after: Span):
        self.before = before
        self.after = after
        self.overlap_percentage = (before._max_bound - after._min_bound + 1) / (before.length() + after.length())


class Engulf:
    def __init__(self, engulfer: Span, engulfee: Span):
        self.engulfer = engulfer
        self.engulfee = engulfee
        self.engulfed_percentage = engulfee.length() / engulfer.length()


class Span:
    __slots__ = ['_min_bound', '_max_bound', 'match']

    def __init__(self, axis: Axis, match: Match):
        if axis == Axis.X:
            self._min_bound = match.x_axis_chromosome_min_idx
            self._max_bound = match.x_axis_chromosome_max_idx
        elif axis == Axis.Y:
            self._min_bound = match.y_axis_chromosome_min_idx
            self._max_bound = match.y_axis_chromosome_max_idx
        else:
            raise ValueError('???')
        assert self._min_bound <= self._max_bound, 'This should never happen'
        self.match = match

    @staticmethod
    def check_overlap(a: Span, b: Span) -> Union[Overlap, Engulf, None]:
        if a._min_bound >= b._min_bound and a._max_bound <= b._max_bound:
            return Engulf(b, a)
        if b._min_bound >= a._min_bound and b._max_bound <= a._max_bound:
            return Engulf(a, b)
        if b._min_bound <= a._min_bound <= b._max_bound:
            return Overlap(b, a)
        if a._min_bound <= b._min_bound <= a._max_bound:
            return Overlap(a, b)
        return None

    def length(self) -> int:
        return (self._max_bound - self._min_bound) + 1  # +1 because min + max are both inclusive, e.g. 0 to 0 has a length of 1

    def __lt__(self, other):
        return (self._min_bound, self._max_bound) < (other._min_bound, other._max_bound)

    def __str__(self):
        return str((self._min_bound, self._max_bound, self.match))

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash((self._min_bound, self._max_bound, self.match))

    def __eq__(self, other):
        return (self._min_bound, self._max_bound, self.match) == (other._min_bound, other._max_bound, other.match)


class MatchAxisIndexer:
    def __init__(self, axis: Axis):
        self.axis = axis
        self.chromosome_spans: Dict[str, List[Span]] = {}

    def index(self, match: Match):
        if self.axis == Axis.X:
            chromosome = match.x_axis_chromosome
        elif self.axis == Axis.Y:
            chromosome = match.y_axis_chromosome
        else:
            raise ValueError('???')
        spans = self.chromosome_spans.setdefault(chromosome, [])
        span = Span(self.axis, match)
        idx = bisect_left(spans, span)
        spans.insert(idx, span)

    def unindex(self, match: Match):
        if self.axis == Axis.X:
            chromosome = match.x_axis_chromosome
        elif self.axis == Axis.Y:
            chromosome = match.y_axis_chromosome
        else:
            raise ValueError('???')
        spans = self.chromosome_spans.setdefault(chromosome, [])
        span = Span(self.axis, match)
        rem_cnt = 0
        while spans:
            idx = bisect_left(spans, span)
            if spans[idx].match == match:
                spans.pop(idx)
                rem_cnt += 1
            else:
                break
        if not spans:
            del self.chromosome_spans[chromosome]
        if rem_cnt == 0:
            raise ValueError('Match does not exist')

    @staticmethod
    def _bisect_left_min_bound(a: List[Span], threshold):
        lo = 0
        hi = len(a)
        while lo < hi:
            mid = (lo + hi) // 2
            if a[mid]._min_bound < threshold:
                lo = mid + 1
            else:
                hi = mid
        return lo

    @staticmethod
    def _bisect_right_max_bound(a: List[Span], threshold):
        lo = 0
        hi = len(a)
        while lo < hi:
            mid = (lo + hi) // 2
            if threshold < a[mid]._max_bound:
                hi = mid
            else:
                lo = mid + 1
        return lo

    def between(self, chromosome: str, min_bound: int, max_bound: int) -> Iterator[Span]:
        if chromosome not in self.chromosome_spans:
            raise ValueError('Chromosome does not exist')
        spans = self.chromosome_spans[chromosome]
        idx1 = MatchAxisIndexer._bisect_left_min_bound(spans, min_bound)
        idx2 = MatchAxisIndexer._bisect_right_max_bound(spans, max_bound)
        return iter(self.chromosome_spans[chromosome][idx1:idx2])

    def walk(self, chromosome: str) -> Iterator[Span]:
        if chromosome not in self.chromosome_spans:
            raise ValueError('Chromosome does not exist')
        return iter(self.chromosome_spans[chromosome])

    def chromosomes(self) -> Set[str]:
        return set(self.chromosome_spans.keys())


if __name__ == '__main__':
    s1 = Span(Axis.Y, Match('Y1', 0, 1, 'X1', 0, 1, MatchType.NORMAL))
    s2 = Span(Axis.Y, Match('Y1', 2, 3, 'X1', 2, 3, MatchType.NORMAL))
    print(f'{Span.check_overlap(s1, s2)}')
    print('----')
    s1 = Span(Axis.Y, Match('Y1', 0, 1, 'X1', 0, 1, MatchType.NORMAL))
    s2 = Span(Axis.Y, Match('Y1', 1, 2, 'X1', 1, 2, MatchType.NORMAL))
    print(f'{Span.check_overlap(s1, s2).before} / {Span.check_overlap(s1, s2).overlap_percentage}')
    print(f'{Span.check_overlap(s1, s2).after} / {Span.check_overlap(s1, s2).after_overlap_percentage}')
    print(f'{Span.check_overlap(s2, s1).before} / {Span.check_overlap(s2, s1).overlap_percentage}')
    print(f'{Span.check_overlap(s2, s1).after} / {Span.check_overlap(s2, s1).after_overlap_percentage}')
    print('----')
    s1 = Span(Axis.Y, Match('Y1', 0, 1, 'X1', 0, 1, MatchType.NORMAL))
    s2 = Span(Axis.Y, Match('Y1', 0, 1, 'X1', 0, 1, MatchType.NORMAL))
    print(f'{Span.check_overlap(s1, s2).engulfer} / {Span.check_overlap(s1, s2).engulfee} / {Span.check_overlap(s1, s2).engulfed_percentage}')
    print(f'{Span.check_overlap(s2, s1).engulfer} / {Span.check_overlap(s2, s1).engulfee} / {Span.check_overlap(s2, s1).engulfed_percentage}')
    print('----')
    s1 = Span(Axis.Y, Match('Y1', 0, 3, 'X1', 0, 3, MatchType.NORMAL))
    s2 = Span(Axis.Y, Match('Y1', 1, 2, 'X1', 1, 2, MatchType.NORMAL))
    print(f'{Span.check_overlap(s1, s2).engulfer} / {Span.check_overlap(s1, s2).engulfee} / {Span.check_overlap(s1, s2).engulfed_percentage}')
    print(f'{Span.check_overlap(s2, s1).engulfer} / {Span.check_overlap(s2, s1).engulfee} / {Span.check_overlap(s2, s1).engulfed_percentage}')
    print('----')
