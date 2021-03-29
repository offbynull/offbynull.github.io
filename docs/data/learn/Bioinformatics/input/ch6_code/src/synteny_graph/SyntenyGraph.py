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


def identify_synteny_blocks(self, matches: Iterable[Match], radius: int = 300):
    min_x = min(m.x_axis_chromosome_min_idx for m in matches)
    max_x = max(m.x_axis_chromosome_max_idx for m in matches)
    min_y = min(m.y_axis_chromosome_min_idx for m in matches)
    max_y = max(m.y_axis_chromosome_max_idx for m in matches)
    y_axis_chromosomes: Set[str] = {m.y_axis_chromosome for m in matches}
    quadtrees: Dict[str, QuadTree] = {chromosome: QuadTree(min_x, max_x, min_y, max_y) for chromosome in y_axis_chromosomes}
    for m in matches:
        quadtrees[m.y_axis_chromosome].add_point(m.x_axis_chromosome_min_idx, m.y_axis_chromosome_min_idx, m)
        quadtrees[m.y_axis_chromosome].add_point(m.x_axis_chromosome_max_idx, m.y_axis_chromosome_max_idx, m)

    for y_axis_chromosome in y_axis_chromosomes:
        quadtree = quadtrees[y_axis_chromosome]
        remaining = {m for m in matches if m.y_axis_chromosome == y_axis_chromosome}
        while remaining:
            x, y, m = next(iter(remaining))
            remaining.remove(m)
            while True:
                # INCOMPLETE / NOT WORKING / NOT TESTED
                # FIX THIS: Scan forward until no more, then backward until no more, then if the distance is large enough consider it a synteny block
                # FIX THIS: Scan forward until no more, then backward until no more, then if the distance is large enough consider it a synteny block
                # FIX THIS: Scan forward until no more, then backward until no more, then if the distance is large enough consider it a synteny block
                # FIX THIS: Scan forward until no more, then backward until no more, then if the distance is large enough consider it a synteny block
                if m.type == MatchType.NORMAL:
                    points = quadtree.get_points_within_radius(
                        m.x_axis_chromosome_max_idx,
                        m.y_axis_chromosome_max_idx,
                        radius
                    )
                elif m.type == MatchType.REVERSE_COMPLEMENT:
                    points = quadtree.get_points_within_radius(
                        m.x_axis_chromosome_min_idx,
                        m.y_axis_chromosome_min_idx,
                        radius
                    )
                else:
                    raise ValueError('???')
                points = {(x, y, next_m) for x, y, next_m in points if next_m.type == m.type and next_m.x_axis_chromosome == m.x_axis_chromosome and (x, y, m) in remaining}
                if not points:
                    break
                closest_point = min(points, key=lambda _x, _y, _: QuadTree.distance(x, _x, y, _y))
                remaining.remove(closest_point)


def plot_raw(
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
    from_chr_colors = {ch: colorsys.hsv_to_rgb(i / len(from_chrs), 1, 0.9) for i, ch in enumerate(from_chrs)}

    to_chromosomes_cnt = len(y_axis_chromosomes)
    plots_per_axis = ceil(sqrt(to_chromosomes_cnt))
    fig, axs = pl.subplots(plots_per_axis, plots_per_axis)
    for ax, to_chr in zip(axs.flatten(), sorted(y_axis_chromosomes)):
        pts = []
        pts_color = []
        for m in filter(lambda m: m.x_axis_chromosome in x_axis_chromosomes and m.y_axis_chromosome == to_chr, matches):
            pts.append([
                (m.x_axis_chromosome_min_idx, m.y_axis_chromosome_min_idx),
                (m.x_axis_chromosome_max_idx, m.y_axis_chromosome_max_idx),
            ])
            pts_color.append(from_chr_colors[m.x_axis_chromosome])
        lc = mc.LineCollection(pts, colors=pts_color, linewidths=2)
        # ax.set_title(to_organism_name + ' CHR ' + to_chr)
        ax.set_xlabel(x_axis_organism_name + ' chrs ' + ('ALL' if x_axis_chromosomes == from_chrs else str(from_chrs)))
        ax.set_ylabel(y_axis_organism_name + ' chr ' + to_chr)
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

    plot_raw(matches, y_axis_organism_name='human', x_axis_organism_name='mouse')
    plt.show()