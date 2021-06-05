from __future__ import annotations

import lzma
import sys
from hashlib import md5

import matplotlib.pyplot as plt

from helpers.InputUtils import str_to_list
from synteny_graph.Match import Match
from synteny_graph.MatchMerger import distance_merge, overlap_filter


def read_genome(l: str):
    genome_chr_files, _ = str_to_list(l, 0)
    genome = {}
    for [chromosome, file] in genome_chr_files:
        with lzma.open(file, mode='rt', encoding='utf-8') as f:
            genome[chromosome] = ''.join([l for l in f.read().split('\n') if not l.startswith('>')])
            genome[chromosome] = genome[chromosome]\
                .replace('R', '')\
                .replace('Y', '')\
                .replace('S', '')\
                .replace('W', '')\
                .replace('K', '')\
                .replace('M', '')\
                .replace('B', '')\
                .replace('D', '')\
                .replace('H', '')\
                .replace('V', '')\
                .replace('N', '')\
                .replace('.', '')\
                .replace('-', '')
    return genome


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        console_input = [l.strip() for l in sys.stdin.readlines()]
        hasher = md5()
        hasher.update('\n'.join(console_input).encode('utf-8'))
        genome1 = read_genome(console_input[0])  # [[C1, /home/user/Downloads/Mycoplasma bovis - GCA_000696015.1_ASM69601v1_genomic.fna]]
        genome2 = read_genome(console_input[1])  # [[C1, /home/user/Downloads/Mycoplasma agalactiae 14628 - GCA_000266865.1_ASM26686v1_genomic.fna]]
        # TODO: include genome1/genome2 data in hasher
        if console_input[2] == 'linear':
            cyclic = False
        elif console_input[2] == 'cyclic':
            cyclic = True
        else:
            raise ValueError('Must be either linear or cyclic')
        k = int(console_input[3])  # 20
        if console_input[4] == 'graph_show':
            show_graph = True
        elif console_input[4] == 'graph_hide':
            show_graph = False
        else:
            raise ValueError(f'Must be entire graph_show or graph_hide')
        print(f'Finding synteny blocks for...\n')
        print(f' * {k=}')
        print(f' * {cyclic=}')
        print(f' * {show_graph=}')
        print(f' * genome1 reference: {console_input[0]}')
        print(f' * genome2 reference: {console_input[1]}')
        print()
        print('NOTE: Nucleotide codes that aren\'t ACGT get filtered out of the genomes.')
        print()
        hash = hasher.hexdigest()

        print(f'Generating genomic dotplot...\n')
        matches = Match.create_from_genomes(20, cyclic, genome1, genome2)
        dp_filename = f'dotplot_{hash}.png'  # changed ext to png because SVG can become super large
        Match.plot(matches)
        # plt.show()
        plt.savefig('/output/' + dp_filename)
        print(f'![Genomic Dot Plot]({dp_filename})\n')

        print(f'Clustering genomic dotplot to snyteny graph...')
        for l in console_input[5:]:
            vals, _ = str_to_list(l.strip(), 0)
            if vals[0] == 'merge':
                radius = int(vals[1])
                angle_half_maw = int(vals[2])
                print(f' * Merging {radius=} {angle_half_maw=}...')
                matches = distance_merge(matches, radius, angle_half_maw)
            elif vals[0] == 'filter':
                max_filter_length = float(vals[1])
                max_merge_distance = float(vals[2])
                print(f' * Filtering {max_filter_length=} {max_merge_distance=}...')
                matches = overlap_filter(matches, max_filter_length, max_merge_distance)
            elif vals[0] == 'cull':
                length = float(vals[1])
                print(f' * Culling below {length=}...')
                matches = [m for m in matches if m.length() >= length]
            else:
                raise ValueError(f'Unrecognized command: {vals}')
        print()

        print(f'Generating synteny graph...\n')
        sg_filename = f'syntenygraph_{hash}.png'  # changed ext to png because SVG can become super large
        Match.plot(matches)
        # plt.show()
        plt.savefig('/output/' + sg_filename)
        print(f'![Synteny Graph]({sg_filename})\n')

        print(f'Mapping synteny graph matches to IDs using x-axis genome...')
        genome1_matches_by_chromosome = {}
        genome2_matches_by_chromosome = {}
        for m in matches:
            genome1_matches_by_chromosome.setdefault(m.y_axis_chromosome, []).append(m)
            genome2_matches_by_chromosome.setdefault(m.x_axis_chromosome, []).append(m)
        for v in genome1_matches_by_chromosome.values():
            v.sort(key=lambda _: _.y_axis_chromosome_min_idx)
        for v in genome2_matches_by_chromosome.values():
            v.sort(key=lambda _: _.x_axis_chromosome_min_idx)
        match_to_id = {}
        for c, m_list in genome2_matches_by_chromosome.items():
            for i, m in enumerate(m_list):
                synteny_id = f'{c}_B{i}'
                match_to_id[m] = synteny_id
                print(f' * {synteny_id} = {m}')
        print()
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()
