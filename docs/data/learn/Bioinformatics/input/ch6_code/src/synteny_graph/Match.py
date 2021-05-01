from __future__ import annotations

import colorsys
import sys
from collections import defaultdict
from enum import Enum
from hashlib import md5
from itertools import product
from math import ceil, sqrt
from typing import Iterable, Optional, Set, List, Dict

import matplotlib.pyplot as plt
import matplotlib.collections as mc
import numpy
import pylab as pl

from helpers.DnaUtils import dna_reverse_complement
from helpers.GeometryUtils import distance
from helpers.Utils import slide_window


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
    def merge(matches: Set[Match]) -> Match:
        assert matches, 'Empty chain'
        first = next(iter(matches))
        y_axis_chromosome = first.y_axis_chromosome
        x_axis_chromosome = first.x_axis_chromosome
        type = first.type
        assert all(y_axis_chromosome == m.y_axis_chromosome
                   and x_axis_chromosome == m.x_axis_chromosome
                   and type == m.type
                   for m in matches), 'Chain type and/or chromosome mismatch'
        # Chain may be unordered -- this is because if the angle maw used to generate the chain extends past 90 degrees,
        # there's a chance that the next item in the chain may go BACKWARD on the x-axis rather than forward. As such,
        # extract the max extents from all the matches and use that to make the merged match.
        x_axis_chromosome_min_idx = min(min(c.x_axis_chromosome_min_idx, c.x_axis_chromosome_max_idx) for c in matches)
        x_axis_chromosome_max_idx = max(max(c.x_axis_chromosome_min_idx, c.x_axis_chromosome_max_idx) for c in matches)
        y_axis_chromosome_min_idx = min(min(c.y_axis_chromosome_min_idx, c.y_axis_chromosome_max_idx) for c in matches)
        y_axis_chromosome_max_idx = max(max(c.y_axis_chromosome_min_idx, c.y_axis_chromosome_max_idx) for c in matches)
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

    def length(self):
        start_pt = self.get_start_point()
        end_pt = self.get_end_point()
        return distance(end_pt[0], start_pt[0], end_pt[1], start_pt[1])

    def clip_x_min(self, x: int) -> Optional[Match]:
        assert self.x_axis_chromosome_max_idx >= x >= self.x_axis_chromosome_min_idx
        if x == self.x_axis_chromosome_max_idx:
            return None
        return Match(
            self.y_axis_chromosome,
            self.y_axis_chromosome_min_idx,
            self.y_axis_chromosome_max_idx,
            self.x_axis_chromosome,
            x,
            self.x_axis_chromosome_max_idx,
            self.type
        )

    def clip_x_max(self, x: int) -> Optional[Match]:
        assert self.x_axis_chromosome_max_idx >= x >= self.x_axis_chromosome_min_idx
        if x == self.x_axis_chromosome_min_idx:
            return None
        return Match(
            self.y_axis_chromosome,
            self.y_axis_chromosome_min_idx,
            self.y_axis_chromosome_max_idx,
            self.x_axis_chromosome,
            self.x_axis_chromosome_min_idx,
            x,
            self.type
        )

    def clip_y_min(self, y: int) -> Optional[Match]:
        assert self.y_axis_chromosome_max_idx >= y >= self.y_axis_chromosome_min_idx
        if y == self.y_axis_chromosome_max_idx:
            return None
        return Match(
            self.y_axis_chromosome,
            y,
            self.y_axis_chromosome_max_idx,
            self.x_axis_chromosome,
            self.x_axis_chromosome_min_idx,
            self.x_axis_chromosome_max_idx,
            self.type
        )

    def clip_y_max(self, y: int) -> Optional[Match]:
        assert self.y_axis_chromosome_max_idx >= y >= self.y_axis_chromosome_min_idx
        if y == self.y_axis_chromosome_min_idx:
            return None
        return Match(
            self.y_axis_chromosome,
            self.y_axis_chromosome_min_idx,
            y,
            self.x_axis_chromosome,
            self.x_axis_chromosome_min_idx,
            self.x_axis_chromosome_max_idx,
            self.type
        )

    def __eq__(self, o: Match) -> bool:
        return (self.y_axis_chromosome, self.y_axis_chromosome_min_idx, self.y_axis_chromosome_max_idx,
                self.x_axis_chromosome, self.x_axis_chromosome_min_idx, self.x_axis_chromosome_max_idx,
                self.type) ==\
               (o.y_axis_chromosome, o.y_axis_chromosome_min_idx, o.y_axis_chromosome_max_idx,
                o.x_axis_chromosome, o.x_axis_chromosome_min_idx, o.x_axis_chromosome_max_idx,
                o.type)

    def __hash__(self) -> int:
        return hash((self.y_axis_chromosome, self.y_axis_chromosome_min_idx, self.y_axis_chromosome_max_idx,
                     self.x_axis_chromosome, self.x_axis_chromosome_min_idx, self.x_axis_chromosome_max_idx,
                     self.type))

    def __str__(self):
        return str({
            'y': (self.y_axis_chromosome, self.y_axis_chromosome_min_idx, self.y_axis_chromosome_max_idx),
            'x': (self.x_axis_chromosome, self.x_axis_chromosome_min_idx, self.x_axis_chromosome_max_idx),
            'type': self.type.name
        })

    def __repr__(self):
        return str(self)

    # MARKDOWN
    @staticmethod
    def create_from_genomes(
            k: int,
            cyclic: bool,  # True if chromosomes are cyclic
            genome1: Dict[str, str],  # chromosome id -> dna string
            genome2: Dict[str, str]   # chromosome id -> dna string
    ) -> List[Match]:
        # lookup tables for data1
        fwd_kmers1 = defaultdict(list)
        rev_kmers1 = defaultdict(list)
        for chr_name, chr_data in genome1.items():
            for kmer, idx in slide_window(chr_data, k, cyclic):
                fwd_kmers1[kmer].append((chr_name, idx))
                rev_kmers1[dna_reverse_complement(kmer)].append((chr_name, idx))
        # lookup tables for data2
        fwd_kmers2 = defaultdict(list)
        rev_kmers2 = defaultdict(list)
        for chr_name, chr_data in genome2.items():
            for kmer, idx in slide_window(chr_data, k, cyclic):
                fwd_kmers2[kmer].append((chr_name, idx))
                rev_kmers2[dna_reverse_complement(kmer)].append((chr_name, idx))
        # match
        matches = []
        fwd_key_matches = set(fwd_kmers1.keys())
        fwd_key_matches.intersection_update(fwd_kmers2.keys())
        for kmer in fwd_key_matches:
            idxes1 = fwd_kmers1.get(kmer, [])
            idxes2 = fwd_kmers2.get(kmer, [])
            for (chr_name1, idx1), (chr_name2, idx2) in product(idxes1, idxes2):
                m = Match(
                    y_axis_chromosome=chr_name1,
                    y_axis_chromosome_min_idx=idx1,
                    y_axis_chromosome_max_idx=idx1 + k - 1,
                    x_axis_chromosome=chr_name2,
                    x_axis_chromosome_min_idx=idx2,
                    x_axis_chromosome_max_idx=idx2 + k - 1,
                    type=MatchType.NORMAL
                )
                matches.append(m)
        rev_key_matches = set(fwd_kmers1.keys())
        rev_key_matches.intersection_update(rev_kmers2.keys())
        for kmer in rev_key_matches:
            idxes1 = fwd_kmers1.get(kmer, [])
            idxes2 = rev_kmers2.get(kmer, [])
            for (chr_name1, idx1), (chr_name2, idx2) in product(idxes1, idxes2):
                m = Match(
                    y_axis_chromosome=chr_name1,
                    y_axis_chromosome_min_idx=idx1,
                    y_axis_chromosome_max_idx=idx1 + k - 1,
                    x_axis_chromosome=chr_name2,
                    x_axis_chromosome_min_idx=idx2,
                    x_axis_chromosome_max_idx=idx2 + k - 1,
                    type=MatchType.REVERSE_COMPLEMENT
                )
                matches.append(m)
        return matches
    # MARKDOWN

    @staticmethod
    def plot(
            matches: Iterable[Match],
            y_axis_organism_name: str = 'to',
            y_axis_chromosomes: Optional[Set[str]] = None,
            x_axis_organism_name: str = 'from',
            x_axis_chromosomes: Optional[Set[str]] = None
    ):
        to_chrs = {m.y_axis_chromosome for m in matches}
        if y_axis_chromosomes is None:
            y_axis_chromosomes = to_chrs
        from_chrs: Set[str] = {m.x_axis_chromosome for m in matches}
        if x_axis_chromosomes is None:
            x_axis_chromosomes = from_chrs
        from_chr_colors = {ch: colorsys.hsv_to_rgb(i / len(from_chrs), 1, 0.9) for i, ch in
                           enumerate(sorted(from_chrs))}

        to_chromosomes_cnt = len(y_axis_chromosomes)
        plots_per_axis = ceil(sqrt(to_chromosomes_cnt))
        fig, axs = pl.subplots(plots_per_axis, plots_per_axis)
        if not isinstance(axs, list):
            axs = numpy.asarray([axs])
        for ax, to_chr in zip(axs.flatten(), sorted(y_axis_chromosomes)):
            pts = []
            pts_color = []
            for m in filter(lambda m: m.x_axis_chromosome in x_axis_chromosomes and m.y_axis_chromosome == to_chr,
                            matches):
                pts.append([m.get_start_point(), m.get_end_point()])
                pts_color.append(from_chr_colors[m.x_axis_chromosome])
            lc = mc.LineCollection(pts, colors=pts_color, linewidths=2)
            # ax.set_title(to_organism_name + ' CHR ' + to_chr)
            ax.set_xlabel(
                x_axis_organism_name + ' chrs ' + ('ALL' if x_axis_chromosomes == from_chrs else str(from_chrs)))
            ax.set_ylabel(y_axis_organism_name + ' chr ' + to_chr)
            # ax.tick_params(axis='both', left=False, top=False, right=False, bottom=False, labelleft=False, labeltop=False, labelright=False, labelbottom=False)
            ax.get_xaxis().get_major_formatter().set_scientific(False)
            ax.get_yaxis().get_major_formatter().set_scientific(False)
            ax.tick_params(axis="y", direction="in", pad=-22)
            ax.tick_params(axis="x", direction="in", pad=-15)
            SET AXIS FROM 0 TO MAX
            SET AXIS FROM 0 TO MAX
            SET AXIS FROM 0 TO MAX
            SET AXIS FROM 0 TO MAX
            SET AXIS FROM 0 TO MAX
            SET AXIS FROM 0 TO MAX
            SET AXIS FROM 0 TO MAX
            SET AXIS FROM 0 TO MAX
            SET AXIS FROM 0 TO MAX
            ax.add_collection(lc)
            ax.autoscale()
            # ax.margins(0.1)

        def on_resize(event):
            fig.tight_layout()
            fig.canvas.draw()

        cid = fig.canvas.mpl_connect('resize_event', on_resize)
        # fig.suptitle('To Chromosomes')


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        console_input = [l.strip() for l in sys.stdin.readlines()]
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
        print(f'Generating genomic dot plot for...\n')
        print(f' * {k=}')
        print(f' * {cyclic=}')
        print(f' * {genome1=}')
        print(f' * {genome2=}\n')
        matches = Match.create_from_genomes(k, cyclic, genome1, genome2)
        Match.plot(matches)
        hasher = md5()
        hasher.update('\n'.join(console_input).encode('utf-8'))
        filename = 'genomicdotplot_' + hasher.hexdigest() + '.svg'
        plt.savefig('/output/' + filename)
        print(f'Result...\n')
        print(f'![Genomic Dot Plot]({filename})\n')
        for m in matches:
            print(f' * {m}')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()