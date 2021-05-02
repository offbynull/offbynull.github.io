from __future__ import annotations

import sys
import tempfile
from collections import defaultdict
from hashlib import md5
from typing import Iterable, List

import matplotlib.pyplot as plt

from helpers.Utils import encode_int_to_alphabet
from synteny_graph.Match import Match, MatchType
from synteny_graph.MatchOverlapClipper import Axis, MatchOverlapClipper
from synteny_graph.MatchSpatialIndexer import MatchSpatialIndexer


# MARKDOWN
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
# MARKDOWN


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


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        console_input = [l.strip() for l in sys.stdin.readlines()]
        hasher = md5()
        hasher.update('\n'.join(console_input).encode('utf-8'))
        hash = hasher.hexdigest()
        k = int(console_input[0])
        if console_input[1] == 'linear':
            cyclic = False
        elif console_input[1] == 'cyclic':
            cyclic = True
        else:
            raise ValueError('2nd line must be either linear or cyclic')
        genome1 = {}
        for name, data in zip(*[iter(console_input[2].strip().split(', '))]*2):
            genome1[name.strip()] = data.strip()
        genome2 = {}
        for name, data in zip(*[iter(console_input[3].strip().split(', '))]*2):
            genome2[name.strip()] = data.strip()
        print(f'Generating synteny graph for...\n')
        print(f' * {k=}')
        print(f' * {cyclic=}')
        print(f' * {genome1=}')
        print(f' * {genome2=}\n')
        matches = Match.create_from_genomes(k, cyclic, genome1, genome2)
        Match.plot(matches)
        filename = f'syntenygraphpre_{hash}.svg'
        plt.savefig('/output/' + filename)
        print(f'Original genomic dot plot...\n')
        print(f'![Genomic Dot Plot]({filename})\n')
        for l in console_input[4:]:
            vals = l.strip().split(', ')
            if vals[0] == 'merge':
                radius = int(vals[1])
                angle_half_maw = int(vals[2])
                print(f'Merging {radius=} {angle_half_maw=}...\n')
                matches = distance_merge(matches, radius, angle_half_maw)
            elif vals[0] == 'filter':
                max_filter_length = float(vals[1])
                max_merge_distance = float(vals[2])
                print(f'Filtering {max_filter_length=} {max_merge_distance=}...\n')
                matches = overlap_filter(matches, max_filter_length, max_merge_distance)
            else:
                raise ValueError(f'Unrecognized command: {vals}')
        Match.plot(matches)
        filename = f'syntenygraphpost_{hash}.svg'
        plt.savefig('/output/' + filename)
        print(f'Final synteny graph...\n')
        print(f'![Synteny Graph]({filename})\n')
        for m in matches:
            print(f' * {m}')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
#     x = tempfile.mktemp()
#     with open(x, 'w') as f:
#         f.write('''7
# linear
# A0, GGATGGTGTCCTCATCTAATGATGTCGGTAAAGAGTCTACCCCGAATGATTATCTGAGTCTCCCATGAACCAAGTCCGTGGTATAGTCCATACTCTGAACCAAAACAGATAAACCAGCAAGATACATTGCAGAAGCTTGCCACCTTAGCAGGTTGTCAGATATCCGTTTCTGGAACTCCCGGGAGGACGATCGGAAGTTGAGCACAGGTACAAACACTTCAGGAATGATCTACTAAACTTTAGGGTCCGTACCTTTTATAATCCTTGCTAGCATCATGTTGAAGGTTAGAGGATTCCGAAACCAGAAGTGGCGATCTCGCTAAAGCAGGTCACCACGGTCAGCGGGTGGCCATTTACTCGTGAAAACCATAGTCCGTGAAAGCTGGGCAACTTTAGTTGGGACCCTTAAGGCGACTGAGGGAAGCAACTATCGGAAGTATCGTACAGGTCGTAAAGTACCAGTACGGAAGAAGCAGGGAGTTATAATATTCACTACCACAATTACCCGAGTTCACTTGTTTCAATCGCCCTCCCTTGACAGAACGTGCGTTACGTAGGAGTGCTTGACATACGGCGGCCGTCTGAGCTAGGACTATCGGAGCGTAATAATGGGATTTCAAATTTACCAGTTCCAGGTTGTCCAAGGGCTTGGCGGTGAGTCGACATGGAAAGATAAATTCCTCAGGTGCTGGCGCTCCCGTGGGGCCGCAGACACTACCTATTGGAGGGTGCTTAAACTATACAGCGCGCTAATTGTTAACTACTCCTTTGTGTCATAAGGGAGGGGAAACACGCGAGGACCGCCTTTGATCTGGTTCAAACGCCTAGAAGTATCTCCATTCTGTCCATTACGCCACCGCCCCGTCGAATGGTACCGGTATCGCTTGACATCTGCTTCTATACTAGAACAACTAATGCCGGCTTCTGGAGTGAAGGCACCATCCCACCAGAGCATTGAAGATTCGCTCGTTGGATTGATAGGAGTGAATATTCTGTCATCTCCTAACTTTTTGGGCACAGCTAG
# B0, CGGCATGGTGTCCTTCATGTGACCTGATGTCCGATAAGGGGGTTCTACGAAGGGCCCTCCACAGGTCCTTTGCCTAAGGATTGTTGGGTCGCATTCAACTGTTACGGAGACGTTACTAGGACGACCTAATAGAACACAACCAAGTTACGTACGCTATATCCTGTCCTGACCCAGTACCCTCTGGGTCTATATAAGTAAGCGGGTACGATTCGAGAGGGGAGCAACCAGTTACAAACACTTCAGGAATCGATCTTACTTAAACTTTTGGGTCCGATACTTTATAATCCTTGCTAGCCTACGATGTTGAGTTGAGGATTCGCGAACCAGAACAATTGCCGATACTCGCTATTAGAGGTCTCCAACGGTCACCGGGTGGGCCATTGACTCGTGAAACCAATAACCGGTGCCATTCGGACAGGGTGCTGTGGCTAGTGAAGTGAATGGCAGATTACGTCTACTGCGTTTGCAACCCAGATCCAAAGGCGTGGCTTCTACGCGTGTTTCCCATCCCTTATCACACAAGAGGGAGTAGTTAACAATTAGCGTGCTGAAGTAGTAAGCCACCCCAATGTTTAGTTCTGCGTGCCCACGGGAGCCAAGCCATCCTGAGGATTTTATGTGTCCATGTCGACAACTACACGGCAAGCACTTAGACAAGCCTGGCAACTGCGTAGAATTATGAAAGCCCACTTATTGCTCCGTATGGTCCGAGCTCAGACGGCCGCCGCTATGTCAAGCACCCCTACGGTTAACGCACGTGTTGTCCAAGGGAAGAGCGGATTGGAGACAAACGTGATCTGCGGGTTAATTGTGGTTAGTGACTATTATTAACCTCCCGTCTTCCTTCCGTCACGGGTAACCTTTACGACCTCATTACGATACTCTCCGATAGGTTGCCTTACCTTCAGTCGCCTAACGGGTCCCAATAAAGTTGCCCGCGTTCTAGGCGAATCATCGCTTGACATCTTGCTTCTTATATACAACCAACCAAATCCCGGCTTCTGGAGCTGAGGCACGCATCCCACCCAGAGGCATTGAAGATTACGCCTCGTTCGGATTGATAGTAGTGCGATATTCTGTATCTCCCTAACTATTTTCGGGCACACTACG
# merge, 4, 45
# merge, 8, 45
# merge, 10, 45
# merge, 15, 45
# filter, 10, 0''')
#     sys.stdin = open(x)
    main()

