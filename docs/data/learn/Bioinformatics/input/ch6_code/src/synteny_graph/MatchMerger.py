from __future__ import annotations

import lzma
from typing import Iterable

import matplotlib.pyplot as plt

from synteny_graph.Match import Match, MatchType
from synteny_graph.MatchAxisIndexer import Axis, MatchAxisIndexer
from synteny_graph.MatchSpatialIndexer import MatchSpatialIndexer


def distance_merge(matches: Iterable[Match], radius: int, angle_half_maw: int = 45):
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


def _encode_int_to_alphabet(number: int, alphabet='ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
    encoded = ''
    sign = ''
    if number < 0:
        sign = '-'
        number = -number
    if 0 <= number < len(alphabet):
        return sign + alphabet[number]
    while number != 0:
        number, i = divmod(number, len(alphabet))
        encoded = alphabet[i] + encoded
    return sign + encoded


THIS WORKS, BUT IT NEEDS TO BE CLEANED UP AND BEFORE COMING IN HERE MATCHES NEED TO BE ADJUSTED/FILTERED SO THERE ARE NO OVERLAPS
THIS WORKS, BUT IT NEEDS TO BE CLEANED UP AND BEFORE COMING IN HERE MATCHES NEED TO BE ADJUSTED/FILTERED SO THERE ARE NO OVERLAPS
THIS WORKS, BUT IT NEEDS TO BE CLEANED UP AND BEFORE COMING IN HERE MATCHES NEED TO BE ADJUSTED/FILTERED SO THERE ARE NO OVERLAPS
THIS WORKS, BUT IT NEEDS TO BE CLEANED UP AND BEFORE COMING IN HERE MATCHES NEED TO BE ADJUSTED/FILTERED SO THERE ARE NO OVERLAPS
THIS WORKS, BUT IT NEEDS TO BE CLEANED UP AND BEFORE COMING IN HERE MATCHES NEED TO BE ADJUSTED/FILTERED SO THERE ARE NO OVERLAPS
THIS WORKS, BUT IT NEEDS TO BE CLEANED UP AND BEFORE COMING IN HERE MATCHES NEED TO BE ADJUSTED/FILTERED SO THERE ARE NO OVERLAPS
THIS WORKS, BUT IT NEEDS TO BE CLEANED UP AND BEFORE COMING IN HERE MATCHES NEED TO BE ADJUSTED/FILTERED SO THERE ARE NO OVERLAPS
THIS WORKS, BUT IT NEEDS TO BE CLEANED UP AND BEFORE COMING IN HERE MATCHES NEED TO BE ADJUSTED/FILTERED SO THERE ARE NO OVERLAPS
THIS WORKS, BUT IT NEEDS TO BE CLEANED UP AND BEFORE COMING IN HERE MATCHES NEED TO BE ADJUSTED/FILTERED SO THERE ARE NO OVERLAPS
THIS WORKS, BUT IT NEEDS TO BE CLEANED UP AND BEFORE COMING IN HERE MATCHES NEED TO BE ADJUSTED/FILTERED SO THERE ARE NO OVERLAPS
THIS WORKS, BUT IT NEEDS TO BE CLEANED UP AND BEFORE COMING IN HERE MATCHES NEED TO BE ADJUSTED/FILTERED SO THERE ARE NO OVERLAPS
THIS WORKS, BUT IT NEEDS TO BE CLEANED UP AND BEFORE COMING IN HERE MATCHES NEED TO BE ADJUSTED/FILTERED SO THERE ARE NO OVERLAPS
THIS WORKS, BUT IT NEEDS TO BE CLEANED UP AND BEFORE COMING IN HERE MATCHES NEED TO BE ADJUSTED/FILTERED SO THERE ARE NO OVERLAPS
THIS WORKS, BUT IT NEEDS TO BE CLEANED UP AND BEFORE COMING IN HERE MATCHES NEED TO BE ADJUSTED/FILTERED SO THERE ARE NO OVERLAPS
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
            span_to_synteny_ids[span.match] = f'{chr_id}_{_encode_int_to_alphabet(i)}'
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
    # matches = []
    # r = Random(111)
    # for x, y in zip(r.sample(range(-100000, 100000), 500), r.sample(range(-100000, 100000), 500)):
    #     match = Match('0', y, y+500, '0', x, x+500, MatchType.NORMAL)
    #     matches.append(match)
    # for x, y in zip(r.sample(range(-100000, 100000), 500), r.sample(range(-100000, 100000), 500)):
    #     match = Match('0', y, y+500, '1', x, x+500, MatchType.REVERSE_COMPLEMENT)
    #     matches.append(match)
    # print(f'{len(matches)}')
    # matches1 = distance_merge(matches, radius=5000, filter_min_len=0)
    # print(f'{len(matches1)}')
    # matches2 = distance_merge(matches, radius=5000, filter_min_len=0)
    # print(f'{len(matches2)}')
    # for a, b in zip(sorted(matches1, key=lambda k: k.x_axis_chromosome_min_idx), sorted(matches2, key=lambda k: k.x_axis_chromosome_min_idx)):
    #     if a.x_axis_chromosome_min_idx != b.x_axis_chromosome_min_idx:
    #         print(f'MISMATCH {a.get_start_point()} vs {b.get_start_point()}')
    # matches = matches2

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
    matches = [m for m in matches if m.y_axis_chromosome == '16']
    # matches = [m for m in matches if m.x_axis_chromosome == '11']
    # matches = [m for m in matches if 57500000 <= m.x_axis_chromosome_min_idx <= 62000000]
    # matches = [m for m in matches if 220000000 <= m.y_axis_chromosome_min_idx <= 240000000]
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
    matches = distance_merge(matches, radius=300000)
    print(f'{len(matches)}')
    matches = distance_merge(matches, radius=300000)
    print(f'{len(matches)}')
    matches = distance_merge(matches, radius=300000)
    print(f'{len(matches)}')
    matches = distance_merge(matches, radius=300000)
    print(f'{len(matches)}')
    matches = [m for m in matches if m.get_length() >= 300000]
    print(f'{len(matches)}')
    matches = distance_merge(matches, radius=500000, angle_half_maw=90)
    print(f'{len(matches)}')
    matches = distance_merge(matches, radius=1000000, angle_half_maw=90)
    print(f'{len(matches)}')
    to_synteny_permutation(matches, Axis.Y, synteny_prefix='HUMAN')
    Match.plot(matches, y_axis_organism_name='human', x_axis_organism_name='mouse')
    plt.show()
