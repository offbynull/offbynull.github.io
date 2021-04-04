from __future__ import annotations

from bisect import bisect_left
from enum import Enum
from typing import List, Dict, Iterator, Set, Union

from synteny_graph.Match import Match, MatchType


class Axis(Enum):
    X = 'X',
    Y = 'Y'

    def chromosome(self, match: Match):
        if self == Axis.X:
            return match.x_axis_chromosome
        elif self == Axis.Y:
            return match.y_axis_chromosome
        else:
            raise ValueError('???')

    def min(self, match: Match):
        if self == Axis.X:
            return match.x_axis_chromosome_min_idx
        elif self == Axis.Y:
            return match.y_axis_chromosome_min_idx
        else:
            raise ValueError('???')

    def max(self, match: Match):
        if self == Axis.X:
            return match.x_axis_chromosome_max_idx
        elif self == Axis.Y:
            return match.y_axis_chromosome_max_idx
        else:
            raise ValueError('???')


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
        self._min_bound = axis.min(match)
        self._max_bound = axis.max(match)
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


class OverlapException(Exception):
    def __init__(self, x_overlap: Union[Engulf, Overlap, None], y_overlap: Union[Engulf, Overlap, None]):
        self.x_overlap = x_overlap
        self.y_overlap = y_overlap


class MatchAxisIndexer:
    def __init__(self):
        self.chromosome_spans: Dict[Axis, Dict[str, List[Span]]] = {
            Axis.X: {},
            Axis.Y: {}
        }

    def index(self, match: Match):
        # find overlaps
        found_overlaps = {Axis.X: [], Axis.Y: []}
        for axis, axis_chromosome_spans in self.chromosome_spans.items():
            chromosome = axis.get_chromosome(match)
            m_min = axis.min(match)
            m_max = axis.max(match)
            overlaps = self._between(axis, chromosome, m_min, m_max)
            if overlaps:
                found_overlaps[axis] = overlaps
        # index overlaps so you can look them up by match
        found_overlaps_lookup = {
            Axis.X: {s.match: s for s in found_overlaps[Axis.X]},
            Axis.Y: {s.match: s for s in found_overlaps[Axis.Y]}
        }
        # does it overlap on both axis?
        for m in found_overlaps_lookup[Axis.X].keys() & found_overlaps_lookup[Axis.Y].keys():
            raise OverlapException(
                Span.check_overlap(found_overlaps_lookup[Axis.X][m], Span(Axis.X, match)),
                Span.check_overlap(found_overlaps_lookup[Axis.Y][m], Span(Axis.Y, match))
            )
        # does it overlap on x axis?
        for m in found_overlaps_lookup[Axis.X].keys():
            raise OverlapException(
                Span.check_overlap(found_overlaps_lookup[Axis.X][m], Span(Axis.X, match)),
                None
            )
        # does it overlap on y axis?
        for m in found_overlaps_lookup[Axis.X].keys():
            raise OverlapException(
                None,
                Span.check_overlap(found_overlaps_lookup[Axis.Y][m], Span(Axis.Y, match))
            )
        # nothing overlaps -- add it
        for axis, axis_chromosome_spans in self.chromosome_spans.items():
            chromosome = axis.get_chromosome(match)
            span = Span(axis, match)
            spans = axis_chromosome_spans.setdefault(chromosome, [])
            idx = bisect_left(spans, span)
            spans.insert(idx, span)

    def unindex(self, match: Match):
        for axis, axis_chromosome_spans in self.chromosome_spans.items():
            chromosome = axis.get_chromosome(match)
            spans = axis_chromosome_spans.setdefault(chromosome, [])
            span = Span(axis, match)
            rem_cnt = 0
            while spans:
                idx = bisect_left(spans, span)
                if spans[idx].match == match:
                    spans.pop(idx)
                    rem_cnt += 1
                else:
                    break
            if not spans:
                del axis_chromosome_spans[chromosome]
            if rem_cnt == 0:
                raise ValueError('Match does not exist')

    def chromosomes(self) -> Set[str]:
        ret = set()
        for v in self.chromosome_spans:
            ret |= v
        return ret

    # def find_overlaps(self) -> Dict[Match, List[Union[Overlap, Engulf]]]:
    #     overlaps: Dict[Match, List[Union[Overlap, Engulf]]] = {}
    #     for c in self.chromosomes():
    #         it = self.walk(c)  # returns iterator that's ordered by min of that axis
    #         s_max_list = [next(it)]
    #         for s_next in it:
    #             new_s_max_list = []
    #             for s_max in s_max_list:
    #                 if s_max._max_bound >= s_next._min_bound:
    #                     new_s_max_list.append(s_max)
    #             s_max_list = new_s_max_list
    #             for s_max in s_max_list:
    #                 overlap = Span.check_overlap(s_next, s_max)
    #                 if overlap is None:
    #                     continue
    #                 overlaps.setdefault(s_max.match, []).append(overlap)
    #                 overlaps.setdefault(s_next.match, []).append(overlap)
    #             s_max_list.append(s_next)
    #     return overlaps

    def walk(self, axis: Axis, chromosome: str) -> Iterator[Span]:
        if chromosome not in self.chromosome_spans:
            raise ValueError('Chromosome does not exist')
        return iter(self.chromosome_spans[chromosome])

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

    def _between(self, axis: Axis, chromosome: str, min_bound: int, max_bound: int) -> List[Span]:
        if chromosome not in self.chromosome_spans[axis]:
            return []
        spans = self.chromosome_spans[axis][chromosome]
        idx1 = MatchAxisIndexer._bisect_left_min_bound(spans, min_bound)
        idx2 = MatchAxisIndexer._bisect_right_max_bound(spans, max_bound)
        return self.chromosome_spans[axis][chromosome][idx1:idx2]


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
