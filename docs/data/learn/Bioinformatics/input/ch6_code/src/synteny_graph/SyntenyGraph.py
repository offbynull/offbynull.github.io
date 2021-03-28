import colorsys
import lzma
from enum import Enum
from math import sqrt, ceil
from typing import Iterable, Set, Dict, Optional

import matplotlib.collections as mc
import matplotlib.pyplot as plt
import pylab as pl

from synteny_graph.QuadTree import QuadTree


class MatchType(Enum):
    NORMAL = 'NORMAL',
    REVERSE_COMPLEMENT = 'REVERSE_COMPLEMENT'


class Match:
    __slots__ = ['to_chromosome', 'to_chromosome_start_idx', 'to_chromosome_end_idx', 'from_chromosome',
                 'from_chromosome_start_idx', 'from_chromosome_end_idx', 'match_type']

    def __init__(
            self,
            to_chromosome: str,
            to_chromosome_start_idx: int,
            to_chromosome_end_idx: int,
            from_chromosome: str,
            from_chromosome_start_idx: int,
            from_chromosome_end_idx: int,
            match_type: MatchType):
        self.to_chromosome = to_chromosome
        self.to_chromosome_start_idx = to_chromosome_start_idx
        self.to_chromosome_end_idx = to_chromosome_end_idx
        self.from_chromosome = from_chromosome
        self.from_chromosome_start_idx = from_chromosome_start_idx
        self.from_chromosome_end_idx = from_chromosome_end_idx
        self.match_type = match_type


class SyntenyGraph:
    def __init__(self, matches: Iterable[Match]):
        min_x = min(min(m.from_chromosome_start_idx, m.from_chromosome_end_idx) for m in matches)
        max_x = max(max(m.from_chromosome_start_idx, m.from_chromosome_end_idx) for m in matches)
        min_y = min(min(m.to_chromosome_start_idx, m.to_chromosome_end_idx) for m in matches)
        max_y = max(max(m.to_chromosome_start_idx, m.to_chromosome_end_idx) for m in matches)
        to_chromosomes: Set[str] = {m.to_chromosome for m in matches}
        # from_chromosomes = {m.from_chromosome for m in matches}
        self.quadtrees: Dict[str, QuadTree] = {chromosome: QuadTree(min_x, max_x, min_y, max_y) for chromosome in to_chromosomes}
        for m in matches:
            self.quadtrees[m.to_chromosome].add_point(m.from_chromosome_start_idx, m.to_chromosome_start_idx, m)
            self.quadtrees[m.to_chromosome].add_point(m.from_chromosome_end_idx, m.to_chromosome_end_idx, m)
        self.matches = list(matches)

    @staticmethod
    def plot_raw(
            matches: Iterable[Match],
            to_organism_name: str = 'to',
            to_chromosomes: Optional[Set[str]] = None,
            from_organism_name: str = 'from',
            from_chromosomes: Optional[Set[str]] = None
    ):
        to_chrs = {m.to_chromosome for m in matches}
        if to_chromosomes is None:
            to_chromosomes = to_chrs
        from_chrs: Set[str] = {m.from_chromosome for m in matches}
        if from_chromosomes is None:
            from_chromosomes = from_chrs
        from_chr_colors = {ch: colorsys.hsv_to_rgb(i / len(from_chrs), 1, 0.9) for i, ch in enumerate(from_chrs)}

        to_chromosomes_cnt = len(to_chromosomes)
        plots_per_axis = ceil(sqrt(to_chromosomes_cnt))
        fig, axs = pl.subplots(plots_per_axis, plots_per_axis)
        for ax, to_chr in zip(axs.flatten(), sorted(to_chromosomes)):
            pts = []
            pts_color = []
            for m in filter(lambda m: m.from_chromosome in from_chromosomes and m.to_chromosome == to_chr, matches):
                pts.append([
                    (m.from_chromosome_start_idx, m.to_chromosome_start_idx),
                    (m.from_chromosome_end_idx, m.to_chromosome_end_idx),
                ])
                pts_color.append(from_chr_colors[m.from_chromosome])
            lc = mc.LineCollection(pts, colors=pts_color, linewidths=2)
            # ax.set_title(to_organism_name + ' CHR ' + to_chr)
            ax.set_xlabel(from_organism_name + ' chrs ' + ('ALL' if from_chromosomes == from_chrs else str(from_chrs)))
            ax.set_ylabel(to_organism_name + ' chr ' + to_chr)
            # ax.tick_params(axis='both', left=False, top=False, right=False, bottom=False, labelleft=False, labeltop=False, labelright=False, labelbottom=False)
            ax.tick_params(axis="y", direction="in", pad=-22)
            ax.tick_params(axis="x", direction="in", pad=-15)
            ax.add_collection(lc)
            ax.autoscale()
            # ax.margins(0.1)

        def on_resize(event):
            fig.tight_layout()
            fig.canvas.draw()
        cid = fig.canvas.mpl_connect('resize_event', on_resize)
        # fig.suptitle('To Chromosomes')


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
            to_chromosome=row[1],
            to_chromosome_start_idx=int(row[2]),
            to_chromosome_end_idx=int(row[3]),
            from_chromosome=row[4],
            from_chromosome_start_idx=int(row[5]),
            from_chromosome_end_idx=int(row[6]),
            match_type=MatchType.NORMAL if row[7] == '+' else MatchType.REVERSE_COMPLEMENT
        )
        matches.append(m)
    lines = []  # no longer required -- clear out memory

    SyntenyGraph.plot_raw(matches, to_organism_name='human', from_organism_name='mouse')
    plt.show()