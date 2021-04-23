from __future__ import annotations

import lzma
from collections import defaultdict
from typing import Iterable, List

import matplotlib.pyplot as plt

from breakpoint_graph import LinearBreakpointGraph
from helpers.Utils import encode_int_to_alphabet
from synteny_graph.Match import Match, MatchType
from synteny_graph.MatchOverlapClipper import Axis, MatchOverlapClipper
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
        found = indexer.scan(m, radius, angle_half_maw)
        merged = Match.merge(found)
        for _m in found:
            indexer.unindex(_m)
            remaining.remove(_m)
        ret.append(merged)
    return ret


def overlap_filter(
        matches: Iterable[Match],
        max_filter_length: float,
        max_merge_distance: float
) -> List[Match]:
    clipper = MatchOverlapClipper(max_filter_length, max_merge_distance)
    for m in matches:
        while True:
            # When you attempt to add a match to the clipper, the clipper may instead ask you to make a set of changes
            # before it'll accept it. Specifically, the clipper may ask you to replace a bunch of existing matches that
            # it's already indexed and then give you a MODIFIED version of m that it'll accept once you've applied
            # those replacements
            changes_requested = clipper.index(m)
            if not changes_requested:
                break
            # replace existing entries in clipper
            for from_m, to_m in changes_requested.existing_matches_to_replace.items():
                clipper.unindex(from_m)
                if to_m:
                    res = clipper.index(to_m)
                    assert res is None
            # replace m with a revised version -- if None it means m isn't needed (its been filtered out)
            m = changes_requested.revised_match
            if not m:
                break
    return list(clipper.get())


def to_synteny_permutation(matches: Iterable[Match], ordered_axis: Axis, synteny_prefix: str = ''):
    matches_sorted_x = sorted(matches, key=lambda m: m.x_axis_chromosome_min_idx)
    matches_sorted_y = sorted(matches, key=lambda m: m.y_axis_chromosome_min_idx)
    chromosome_lookup_x = defaultdict(list)
    chromosome_lookup_y = defaultdict(list)
    # Create synteny block IDs for matches
    if ordered_axis == Axis.X:
        ordered_matches = matches_sorted_x
        for m in ordered_matches:
            chromosome_lookup_x[m.x_axis_chromosome].append(m)
            chromosome_lookup_y[m.y_axis_chromosome].append(m)
        ordered_chromosome_lookup = chromosome_lookup_x
    elif ordered_axis == Axis.Y:
        ordered_matches = matches_sorted_y
        for m in ordered_matches:
            chromosome_lookup_x[m.x_axis_chromosome].append(m)
            chromosome_lookup_y[m.y_axis_chromosome].append(m)
        ordered_chromosome_lookup = chromosome_lookup_y
    else:
        raise ValueError('???')
    match_to_synteny_ids = {}
    for chr_id in sorted(ordered_chromosome_lookup.keys()):
        for i, match in enumerate(ordered_chromosome_lookup[chr_id]):
            match_to_synteny_ids[match] = f'{chr_id}_{encode_int_to_alphabet(i)}'
    # Create permutations for each species chromosome
    x_chromosome_perms = defaultdict(list)
    for chr_id in sorted(chromosome_lookup_x.keys()):
        perm = x_chromosome_perms[chr_id]
        for match in chromosome_lookup_x[chr_id]:
            synteny_id = synteny_prefix + '_' + match_to_synteny_ids[match]
            if matches_sorted_x is ordered_matches:
                perm.append('+' + synteny_id)
            else:
                if match.type == MatchType.NORMAL:
                    perm.append('+' + synteny_id)
                elif match.type == MatchType.REVERSE_COMPLEMENT:
                    perm.append('-' + synteny_id)
                else:
                    raise ValueError('???')
    y_chromosome_perms = defaultdict(list)
    for chr_id in sorted(chromosome_lookup_y.keys()):
        perm = y_chromosome_perms.setdefault(chr_id, [])
        for match in chromosome_lookup_y[chr_id]:
            synteny_id = synteny_prefix + '_' + match_to_synteny_ids[match]
            if matches_sorted_y == ordered_matches:
                perm.append('+' + synteny_id)
            else:
                if match.type == MatchType.NORMAL:
                    perm.append('+' + synteny_id)
                elif match.type == MatchType.REVERSE_COMPLEMENT:
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
    matches = [m for m in matches if m.y_axis_chromosome in {'1', '2'}]
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
    matches = distance_merge(matches, radius=100000)
    print(f'{len(matches)}')
    matches = [m for m in matches if m.length() >= 100000]
    print(f'{len(matches)}')
    matches = distance_merge(matches, radius=200000)
    print(f'{len(matches)}')
    matches = distance_merge(matches, radius=300000)
    print(f'{len(matches)}')
    matches = distance_merge(matches, radius=400000)
    print(f'{len(matches)}')
    matches = distance_merge(matches, radius=500000)
    print(f'{len(matches)}')
    matches = overlap_filter(matches, max_filter_length=1000000, max_merge_distance=5000000)
    print(f'{len(matches)}')
    human_perms, mouse_perms = to_synteny_permutation(matches, Axis.Y, synteny_prefix='HUMAN')
    print(f'{human_perms}')
    print(f'{mouse_perms}')

    bg = LinearBreakpointGraph.BreakpointGraph(
        [mouse_perms[ch] for ch in sorted(mouse_perms.keys())],
        [human_perms[ch] for ch in sorted(human_perms.keys())]
    )
    print(bg.to_neato_graph())
    print(bg.red_permutations)
    while True:
        next_blue_edge_to_break_on = bg.find_blue_edge_in_non_trivial_path()
        if next_blue_edge_to_break_on is None:
            break
        bg.two_break(next_blue_edge_to_break_on)
        print(bg.red_permutations)
        print(bg.to_neato_graph())

    Match.plot(matches, y_axis_organism_name='human', x_axis_organism_name='mouse')
    plt.show()
