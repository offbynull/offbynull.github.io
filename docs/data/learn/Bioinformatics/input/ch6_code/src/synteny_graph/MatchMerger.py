from __future__ import annotations

import lzma
from typing import Iterable, List

import matplotlib.pyplot as plt

from helpers.Utils import encode_int_to_alphabet
from synteny_graph.Match import Match, MatchType
from synteny_graph.MatchAxisIndexer import Axis, MatchAxisIndexer, Span, Overlap, Engulf
from synteny_graph.MatchSpatialIndexer import MatchSpatialIndexer


def distance_merge(matches: Iterable[Match], radius: int, angle_half_maw: int = 45) -> List[Match]:
    min_x = min(m.x_axis_chromosome_min_idx for m in matches)
    max_x = max(m.x_axis_chromosome_max_idx for m in matches)
    min_y = min(m.y_axis_chromosome_min_idx for m in matches)
    max_y = max(m.y_axis_chromosome_max_idx for m in matches)
    indexer = MatchSpatialIndexer(min_x, max_x, min_y, max_y)
    for m in matches:
        indexer.index(m)
    ret = []
    remaining = set(matches)
    while remaining:
        m = next(iter(remaining))
        chain = indexer.scan(m, radius, angle_half_maw)
        merged = Match.merge(chain)
        for _m in chain:
            indexer.unindex(_m)
            remaining.remove(_m)
        ret.append(merged)
    return ret


FINISH FIXING UP MATCHAXISINDEXER, RENAME THIS TO OVERLAP_MERGE(), THEN REIMPLEMENT IT TO USE THE NEW MATCHAXISINDEXER
FINISH FIXING UP MATCHAXISINDEXER, RENAME THIS TO OVERLAP_MERGE(), THEN REIMPLEMENT IT TO USE THE NEW MATCHAXISINDEXER
FINISH FIXING UP MATCHAXISINDEXER, RENAME THIS TO OVERLAP_MERGE(), THEN REIMPLEMENT IT TO USE THE NEW MATCHAXISINDEXER
FINISH FIXING UP MATCHAXISINDEXER, RENAME THIS TO OVERLAP_MERGE(), THEN REIMPLEMENT IT TO USE THE NEW MATCHAXISINDEXER
FINISH FIXING UP MATCHAXISINDEXER, RENAME THIS TO OVERLAP_MERGE(), THEN REIMPLEMENT IT TO USE THE NEW MATCHAXISINDEXER
FINISH FIXING UP MATCHAXISINDEXER, RENAME THIS TO OVERLAP_MERGE(), THEN REIMPLEMENT IT TO USE THE NEW MATCHAXISINDEXER
FINISH FIXING UP MATCHAXISINDEXER, RENAME THIS TO OVERLAP_MERGE(), THEN REIMPLEMENT IT TO USE THE NEW MATCHAXISINDEXER
FINISH FIXING UP MATCHAXISINDEXER, RENAME THIS TO OVERLAP_MERGE(), THEN REIMPLEMENT IT TO USE THE NEW MATCHAXISINDEXER
FINISH FIXING UP MATCHAXISINDEXER, RENAME THIS TO OVERLAP_MERGE(), THEN REIMPLEMENT IT TO USE THE NEW MATCHAXISINDEXER
def check_and_filter(
        matches: Iterable[Match],
        min_allowable_len: float = 0.0,
        max_allowed_overlap_percent: float = 0.05,
        max_prunable_engulf_percent: float = 0.05
) -> List[Match]:
    def __do(matches, axis):
        indexer = MatchAxisIndexer(axis)
        for m in matches:
            indexer.index(m)
        ret = []
        for c in indexer.chromosomes():
            it = indexer.walk(c)  # returns iterator that's ordered by min of that axis
            it = filter(lambda s: s.length() >= min_allowable_len, it)  # make iterator ignore anything < min_length
            ret.append(next(it))  # add first iterator item
            for s in it:
                o = Span.check_overlap(ret[-1], s)  # check if span to be added crosses boundaries of prev span
                if o is None:  # no crossed boundaries, skip
                    ...
                elif isinstance(o, Overlap):  # if overlaps, only allow it it through if its within a certain threshold
                    if o.overlap_percentage > max_allowed_overlap_percent:
                        raise ValueError(f'Overlap {o.overlap_percentage} >= {max_allowed_overlap_percent}: {o.before} vs {o.after}')
                elif isinstance(o, Engulf):  # if totally engulfs, remove the one that's under a certain threshold
                    if o.engulfed_percentage >= max_prunable_engulf_percent:
                        raise ValueError(f'Engulfed {o.engulfed_percentage} >= {max_prunable_engulf_percent}: {o.engulfer} vs {o.engulfee}')
                    if o.engulfee is ret[-1]:  # prev span is totally engulfed, remove it.
                        ret.pop()
                    elif o.engulfee is s:   # span to be added is totally engulfed, skip adding it.
                        continue
                    else:
                        raise ValueError('???')
                else:
                    raise ValueError('???')
                ret.append(s)
        return [s.match for s in ret]
    matches = __do(matches, Axis.X)
    matches = __do(matches, Axis.Y)
    return matches


def to_synteny_permutation(matches: Iterable[Match], ordered_axis: Axis, synteny_prefix: str = ''):
    x_indexer = MatchAxisIndexer(Axis.X)
    y_indexer = MatchAxisIndexer(Axis.Y)
    for s in matches:
        x_indexer.index(s)
        y_indexer.index(s)
    # Create synteny block IDs for matches
    if ordered_axis == Axis.X:
        ordered_indexer = x_indexer
    elif ordered_axis == Axis.Y:
        ordered_indexer = y_indexer
    else:
        raise ValueError('???')
    span_to_synteny_ids = {}
    for chr_id in ordered_indexer.chromosomes():
        for i, span in enumerate(ordered_indexer.walk(chr_id)):
            span_to_synteny_ids[span.match] = f'{chr_id}_{encode_int_to_alphabet(i)}'
    # Create permutations for each species chromosome
    x_chromosome_perms = {}
    for chr_id in x_indexer.chromosomes():
        perm = x_chromosome_perms.setdefault(chr_id, [])
        for span in x_indexer.walk(chr_id):
            synteny_id = synteny_prefix + '_' + span_to_synteny_ids[span.match]
            if x_indexer == ordered_indexer:
                perm.append('+' + synteny_id)
            else:
                if span.match.type == MatchType.NORMAL:
                    perm.append('+' + synteny_id)
                elif span.match.type == MatchType.REVERSE_COMPLEMENT:
                    perm.append('-' + synteny_id)
                else:
                    raise ValueError('???')
    y_chromosome_perms = {}
    for chr_id in y_indexer.chromosomes():
        perm = y_chromosome_perms.setdefault(chr_id, [])
        for span in y_indexer.walk(chr_id):
            synteny_id = synteny_prefix + '_' + span_to_synteny_ids[span.match]
            if y_indexer == ordered_indexer:
                perm.append('+' + synteny_id)
            else:
                if span.match.type == MatchType.NORMAL:
                    perm.append('+' + synteny_id)
                elif span.match.type == MatchType.REVERSE_COMPLEMENT:
                    perm.append('-' + synteny_id)
                else:
                    raise ValueError('???')
    # Return -- first element will always be the ordered axis
    if ordered_axis == Axis.X:
        return x_chromosome_perms, y_chromosome_perms
    elif ordered_axis == Axis.Y:
        return y_chromosome_perms, x_chromosome_perms
    else:
        raise ValueError('???')


if __name__ == '__main__':
    with lzma.open('../anchors_human_mouse.txt.xz', mode='rt', encoding='utf-8') as f:
        data = str(f.read())
    lines = data.strip().split('\n')
    lines = lines[1:]
    matches = []
    for line in lines:
        line = line.strip()
        row = line.split(' ')
        m = Match(
            y_axis_chromosome=row[1],
            y_axis_chromosome_min_idx=int(row[2]),
            y_axis_chromosome_max_idx=int(row[3]),
            x_axis_chromosome=row[4],
            x_axis_chromosome_min_idx=int(row[5]),
            x_axis_chromosome_max_idx=int(row[6]),
            type=MatchType.NORMAL if row[7] == '+' else MatchType.REVERSE_COMPLEMENT
        )
        matches.append(m)
    lines = []  # no longer required -- clear out memory
    matches = [m for m in matches if m.y_axis_chromosome == '2']
    # matches = [m for m in matches if m.x_axis_chromosome == '1']
    # matches = random.sample(matches, len(matches) // 10)
    print(f'{len(matches)}')
    matches = distance_merge(matches, radius=10000)
    print(f'{len(matches)}')
    matches = distance_merge(matches, radius=20000)
    print(f'{len(matches)}')
    matches = distance_merge(matches, radius=30000)
    print(f'{len(matches)}')
    matches = distance_merge(matches, radius=40000)
    print(f'{len(matches)}')
    matches = distance_merge(matches, radius=50000)
    print(f'{len(matches)}')
    matches = distance_merge(matches, radius=60000)
    print(f'{len(matches)}')
    matches = distance_merge(matches, radius=70000)
    print(f'{len(matches)}')
    matches = distance_merge(matches, radius=80000)
    print(f'{len(matches)}')
    matches = distance_merge(matches, radius=90000)
    print(f'{len(matches)}')
    matches = distance_merge(matches, radius=100000, angle_half_maw=135)
    print(f'{len(matches)}')
    matches = [m for m in matches if m.length() >= 100000]
    print(f'{len(matches)}')
    matches = distance_merge(matches, radius=200000, angle_half_maw=135)
    print(f'{len(matches)}')
    matches = distance_merge(matches, radius=300000, angle_half_maw=135)
    print(f'{len(matches)}')
    matches = distance_merge(matches, radius=400000, angle_half_maw=135)
    print(f'{len(matches)}')
    matches = distance_merge(matches, radius=500000, angle_half_maw=135)
    print(f'{len(matches)}')
    matches = distance_merge(matches, radius=600000, angle_half_maw=135)
    print(f'{len(matches)}')
    matches = distance_merge(matches, radius=700000, angle_half_maw=135)
    print(f'{len(matches)}')
    matches = distance_merge(matches, radius=800000, angle_half_maw=135)
    print(f'{len(matches)}')
    matches = distance_merge(matches, radius=900000, angle_half_maw=135)
    print(f'{len(matches)}')
    matches = distance_merge(matches, radius=1000000, angle_half_maw=135)
    print(f'{len(matches)}')
    matches = overlap_merge(matches, max_allowed_overlap_percent=0.1, max_prunable_engulf_percent=0.1)
    print(f'{len(matches)}')
    to_synteny_permutation(matches, Axis.Y, synteny_prefix='HUMAN')
    Match.plot(matches, y_axis_organism_name='human', x_axis_organism_name='mouse')
    plt.show()
