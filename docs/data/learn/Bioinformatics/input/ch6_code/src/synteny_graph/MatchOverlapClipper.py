from __future__ import annotations

from bisect import bisect_left
from enum import Enum
from typing import List, Dict, Set, Tuple, SupportsFloat, Optional

from helpers.GeometryUtils import slope, y_intercept, line_intercept, distance, perpendicular_line
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


class Span:
    __slots__ = ['_min_bound', '_max_bound', 'match']

    def __init__(self, axis: Axis, match: Match):
        self._min_bound = axis.min(match)
        self._max_bound = axis.max(match)
        assert self._min_bound <= self._max_bound, 'This should never happen'
        self.match = match

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
    def __init__(self, match: Match, axises: Set[Axis]):
        self.match = match
        self.axises = axises


# This class makes a best effort to get rid of overlapping matches. If a match overlaps, it will the following
# operations in the following order to reduce the overlap:
#  1. Is one of the matches <= a certain length? If so get rid of that match (leaving a single match -- no more overlap)
#  2. Are the overlapping matches sandwiched together closely (within a certain distance)? If so merge them together
#     into a single match (no more overlap)
#  3. Clip one of the overlapping matches such that the overlap no longer exists between them. The longer match is the
#     one that gets clipped.
class MatchOverlapClipper:
    def __init__(self, max_filter_length: float, max_merge_distance: float):
        self.max_filter_length = max_filter_length
        self.max_merge_distance = max_merge_distance
        self.chromosome_spans: Dict[Axis, Dict[str, List[Span]]] = {
            Axis.X: {},
            Axis.Y: {}
        }

    def index(self, match: Match):
        # find overlaps within the same chromosomes
        found_overlaps = {a: set() for a in Axis}
        for axis, axis_chromosome_spans in self.chromosome_spans.items():
            chromosome = axis.chromosome(match)
            m_min = axis.min(match)
            m_max = axis.max(match)
            overlaps = self._between(axis, chromosome, m_min, m_max)
            if overlaps:
                found_overlaps[axis] = {s.match for s in overlaps}
        # does it overlap? -- try different heuristics until its gone
        bad_match: Optional[Match] = next(iter(found_overlaps[Axis.X] | found_overlaps[Axis.Y]), None)
        if bad_match is not None:  # 1. is the offending match small enough to be filtered out?
            remove1, remove2 = MatchOverlapClipper.overlap_filter_metric(match, bad_match, self.max_filter_length)
            if remove1 and remove2:  # don't add match and remove bad_match
                self.unindex(bad_match)
                return
            if remove2:  # add match but remove bad_match
                self.unindex(bad_match)
                bad_match = None
            if remove1:  # don't add match but keep bad_match
                return
        if bad_match is not None:  # 2. can the overlaps be merged?
            dist = MatchOverlapClipper.overlap_closeness_metric(match, bad_match)
            if dist <= self.max_merge_distance and match.type == bad_match.type:
                match = Match.merge({match, bad_match})
                self.unindex(bad_match)
                bad_match = None
        if bad_match is not None:  # 3. can the overlapping parts be clipped off? if so do it
            new_match, new_bad_match = MatchOverlapClipper.best_effort_overlap_clip(match, bad_match)
            self.unindex(bad_match)  # replace bad_match with clipped one (it may have clipped out of existence -- None)
            if new_bad_match:
                self.index(new_bad_match)
            bad_match = new_bad_match
            if new_match:  # replace match with clipped one (it may have clipped out of existence -- None, if so return)
                match = new_match
            else:
                return
        # add it in
        for axis, axis_chromosome_spans in self.chromosome_spans.items():
            chromosome = axis.chromosome(match)
            span = Span(axis, match)
            spans = axis_chromosome_spans.setdefault(chromosome, [])
            idx = bisect_left(spans, span)
            spans.insert(idx, span)

    def unindex(self, match: Match):
        for axis, axis_chromosome_spans in self.chromosome_spans.items():
            chromosome = axis.chromosome(match)
            spans = axis_chromosome_spans.setdefault(chromosome, [])
            span = Span(axis, match)
            rem_cnt = 0
            while spans:
                idx = bisect_left(spans, span)
                if idx != len(spans) and spans[idx].match == match:
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

    def walk(self) -> Set[Match]:
        ret = set()
        for axis, axis_chromosome_spans in self.chromosome_spans.items():
            for chromosome, spans in axis_chromosome_spans.items():
                for s in spans:
                    ret.add(s.match)
        return ret

    @staticmethod
    def _find_max_ge_threshold(a: List[Span], threshold: int):
        # bisect left
        lo = 0
        hi = len(a)
        while lo < hi:
            mid = (lo + hi) // 2
            if a[mid]._max_bound < threshold:
                lo = mid + 1
            else:
                hi = mid
        # return lo
        return lo if lo != len(a) else -1

    @staticmethod
    def _find_min_le_threshold(a: List[Span], threshold: int):
        # bisect right
        lo = 0
        hi = len(a)
        while lo < hi:
            mid = (lo + hi) // 2
            if threshold < a[mid]._min_bound:
                hi = mid
            else:
                lo = mid + 1
        # return lo
        return lo-1 if lo else -1

    def _between(self, axis: Axis, chromosome: str, min_bound: int, max_bound: int) -> List[Span]:
        if chromosome not in self.chromosome_spans[axis]:
            return []
        spans = self.chromosome_spans[axis][chromosome]
        idx1 = MatchOverlapClipper._find_max_ge_threshold(spans, min_bound)
        idx2 = MatchOverlapClipper._find_min_le_threshold(spans, max_bound)
        if idx1 != -1 and idx2 != -1 and idx1 <= idx2:
            return self.chromosome_spans[axis][chromosome][idx1:idx2+1]
        else:
            return []

    @staticmethod
    def _perpendicular_distance(pt: Tuple[SupportsFloat, SupportsFloat], match: Match) -> float:
        m = slope(
            match.get_start_point()[0],
            match.get_end_point()[0],
            match.get_start_point()[1],
            match.get_end_point()[1]
        )
        b = y_intercept(
            match.get_start_point()[0],
            match.get_start_point()[1],
            match.get_end_point()[0],
            match.get_end_point()[1]
        )
        m_inv, b_inv = perpendicular_line(m, pt)
        x, y = line_intercept(m, b, m_inv, b_inv)
        return distance(x, pt[0], y, pt[1])

    @staticmethod
    def overlap_closeness_metric(m1: Match, m2: Match) -> float:
        if m1.x_axis_chromosome_min_idx > m2.x_axis_chromosome_min_idx:
            d1 = MatchOverlapClipper._perpendicular_distance(m1.get_start_point(), m2)
        else:
            d1 = MatchOverlapClipper._perpendicular_distance(m2.get_start_point(), m1)
        if m1.x_axis_chromosome_max_idx < m2.x_axis_chromosome_max_idx:
            d2 = MatchOverlapClipper._perpendicular_distance(m1.get_end_point(), m2)
        else:
            d2 = MatchOverlapClipper._perpendicular_distance(m2.get_end_point(), m1)
        return (d1 + d2) / 2

    @staticmethod
    def overlap_filter_metric(m1: Match, m2: Match, len_threshold: float) -> Tuple[bool, bool]:
        if m1.length() <= len_threshold and m2.length() <= len_threshold:
            return True, True
        if m2.length() <= len_threshold:
            return False, True
        if m1.length() <= len_threshold:
            return True, False
        return False, False

    @staticmethod
    def best_effort_overlap_clip(m1: Match, m2: Match) -> Tuple[Optional[Match], Optional[Match]]:
        # X OVERLAP CLIP
           # do the xs totally overlap? keep one (doesn't matter which)
        if m1.x_axis_chromosome_min_idx == m2.x_axis_chromosome_min_idx\
                and m1.x_axis_chromosome_max_idx == m2.x_axis_chromosome_max_idx:
            return m1, None
           # is x overlapped where m1 starts after m2?
        if m2.x_axis_chromosome_min_idx <= m1.x_axis_chromosome_min_idx <= m2.x_axis_chromosome_max_idx:
            if m1.length() > m2.length():
                m1 = m1.clip_x_min(m2.x_axis_chromosome_max_idx + 1)
            else:
                m2 = m2.clip_x_max(m1.x_axis_chromosome_min_idx - 1)
          # is x overlapped where m1 starts after m2?
        elif m1.x_axis_chromosome_min_idx <= m2.x_axis_chromosome_min_idx <= m1.x_axis_chromosome_max_idx:
            if m1.length() > m2.length():
                m1 = m1.clip_x_max(m2.x_axis_chromosome_min_idx - 1)
            else:
                m2 = m2.clip_x_min(m1.x_axis_chromosome_max_idx + 1)
          # did one of the matches get clipped to nothing? done.
        if m1 is None or m2 is None:
            return m1, m2
        # Y OVERLAP CLIP
           # do the ys totally overlap? keep one (doesn't matter which)
        if m1.y_axis_chromosome_min_idx == m2.y_axis_chromosome_min_idx\
                and m1.y_axis_chromosome_max_idx == m2.y_axis_chromosome_max_idx:
            return m1, None
           # is y overlapped where m1 starts after m2?
        if m2.y_axis_chromosome_min_idx <= m1.y_axis_chromosome_min_idx <= m2.y_axis_chromosome_max_idx:
            if m1.length() > m2.length():
                m1 = m1.clip_y_min(m2.y_axis_chromosome_max_idx + 1)
            else:
                m2 = m2.clip_y_max(m1.y_axis_chromosome_min_idx - 1)
          # is y overlapped where m1 starts after m2?
        elif m1.y_axis_chromosome_min_idx <= m2.y_axis_chromosome_min_idx <= m1.y_axis_chromosome_max_idx:
            if m1.length() > m2.length():
                m1 = m1.clip_y_max(m2.y_axis_chromosome_min_idx - 1)
            else:
                m2 = m2.clip_y_min(m1.y_axis_chromosome_max_idx + 1)
          # did one of the matches get clipped to nothing? done. -- COMMENTED OUT BECAUSE RETURN IMMEDIATELY AFTER
        # if m1 is None or m2 is None:
        #     return m1, m2
        return m1, m2


if __name__ == '__main__':
    x = MatchOverlapClipper()
    x.index(Match('Y1', 0, 1, 'X1', 0, 1, MatchType.NORMAL))
    x.index(Match('Y1', 4, 5, 'X1', 4, 5, MatchType.NORMAL))
    x.index(Match('Y1', 2, 3, 'X1', 2, 3, MatchType.NORMAL))
    # x.index(Match('Y1', 4, 5, 'X1', 4, 5, MatchType.NORMAL))  # should overlap -- ok
    # x.index(Match('Y1', 2, 3, 'X1', 2, 3, MatchType.NORMAL))  # should overlap -- ok
    # x.index(Match('Y1', 0, 1, 'X1', 0, 1, MatchType.NORMAL))  # should overlap -- ok
    # x.index(Match('Y1', 0, 2, 'X1', 0, 2, MatchType.NORMAL))  # should overlap -- ok
    # x.index(Match('Y1', 1, 2, 'X1', 1, 2, MatchType.NORMAL))  # should overlap -- ok
    # x.index(Match('Y1', 0, 3, 'X1', 0, 3, MatchType.NORMAL))  # should overlap -- ok

    # m1 = Match('3', 99725203, 109775486, '16', 48857864, 58896953, MatchType.REVERSE_COMPLEMENT)
    # m2 = Match('3', 94886705, 99743622, '16', 58880039, 63295838, MatchType.REVERSE_COMPLEMENT)
    # MatchOverlapIndexer.overlap_closeness_metric(m1, m2)

    m1 = Match('A', 0, 9, 'B', 0, 9, MatchType.REVERSE_COMPLEMENT)
    m2 = Match('A', 10, 19, 'B', 5, 15, MatchType.REVERSE_COMPLEMENT)
    m1, m2 = MatchOverlapClipper.best_effort_overlap_clip(m1, m2)
    print(f'{m1=} {m2=}')

    m1 = Match('A', 0, 9, 'B', 0, 9, MatchType.REVERSE_COMPLEMENT)
    m2 = Match('A', 10, 19, 'B', 5, 11, MatchType.REVERSE_COMPLEMENT)
    m1, m2 = MatchOverlapClipper.best_effort_overlap_clip(m1, m2)
    print(f'{m1=} {m2=}')

    m1 = Match('A', 8, 9, 'B', 10, 19, MatchType.REVERSE_COMPLEMENT)
    m2 = Match('A', 0, 9, 'B', 20, 29, MatchType.REVERSE_COMPLEMENT)
    m1, m2 = MatchOverlapClipper.best_effort_overlap_clip(m1, m2)
    print(f'{m1=} {m2=}')

    m1 = Match('A', 2, 9, 'B', 10, 19, MatchType.REVERSE_COMPLEMENT)
    m2 = Match('A', 0, 9, 'B', 20, 29, MatchType.REVERSE_COMPLEMENT)
    m1, m2 = MatchOverlapClipper.best_effort_overlap_clip(m1, m2)
    print(f'{m1=} {m2=}')

    m1 = Match('A', 0, 9, 'B', 10, 19, MatchType.REVERSE_COMPLEMENT)
    m2 = Match('A', 0, 9, 'B', 20, 29, MatchType.REVERSE_COMPLEMENT)
    m1, m2 = MatchOverlapClipper.best_effort_overlap_clip(m1, m2)
    print(f'{m1=} {m2=}')

    m1 = Match('A', 10, 19, 'B', 0, 9, MatchType.REVERSE_COMPLEMENT)
    m2 = Match('A', 20, 29, 'B', 0, 9, MatchType.REVERSE_COMPLEMENT)
    m1, m2 = MatchOverlapClipper.best_effort_overlap_clip(m1, m2)
    print(f'{m1=} {m2=}')
