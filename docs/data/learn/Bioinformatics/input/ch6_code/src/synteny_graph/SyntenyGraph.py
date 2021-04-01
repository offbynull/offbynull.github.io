from __future__ import annotations

import colorsys
import lzma
from math import sqrt, ceil
from typing import Iterable, Set, Optional

import matplotlib.collections as mc
import matplotlib.pyplot as plt
import numpy
import pylab as pl

from synteny_graph.Match import Match, MatchType
from synteny_graph.MatchIndexer import MatchIndexer


def distance_merge(matches: Iterable[Match], radius: int, filter_min_len: int):
    min_x = min(m.x_axis_chromosome_min_idx for m in matches)
    max_x = max(m.x_axis_chromosome_max_idx for m in matches)
    min_y = min(m.y_axis_chromosome_min_idx for m in matches)
    max_y = max(m.y_axis_chromosome_max_idx for m in matches)
    indexer = MatchIndexer(min_x, max_x, min_y, max_y)

    for m in matches:
        indexer.index(m)

    ret = []
    remaining = set(matches)
    while remaining:
        m = next(iter(remaining))
        chain = indexer.scan(m, radius)
        # if it didn't result in a larger chain, remove it from consideration and add it to the result set
        if chain == [m]:
            indexer.unindex(m)
            remaining.remove(m)
            if m.get_length() >= filter_min_len:
                ret.append(m)
            continue
        # merge the chain, then substitute merged in for the chained matches used to create it
        merged = Match.merge(chain)
        for _m in chain:
            indexer.unindex(_m)
            remaining.remove(_m)
        indexer.index(merged)
        remaining.add(merged)
    return ret


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
    if not isinstance(axs, list):
        axs = numpy.asarray([axs])
    for ax, to_chr in zip(axs.flatten(), sorted(y_axis_chromosomes)):
        pts = []
        pts_color = []
        for m in filter(lambda m: m.x_axis_chromosome in x_axis_chromosomes and m.y_axis_chromosome == to_chr, matches):
            pts.append([m.get_start_point(), m.get_end_point()])
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

    matches = [m for m in matches if m.y_axis_chromosome == '2']
    # matches = random.sample(matches, len(matches) // 10)
    print(f'{len(matches)}')
    matches = distance_merge(matches, radius=10000, filter_min_len=0)
    print(f'{len(matches)}')
    matches = distance_merge(matches, radius=10000, filter_min_len=0)
    print(f'{len(matches)}')
    matches = distance_merge(matches, radius=10000, filter_min_len=0)
    print(f'{len(matches)}')
    matches = distance_merge(matches, radius=10000, filter_min_len=0)
    print(f'{len(matches)}')
    # matches = distance_merge(matches, radius=20000, filter_min_len=0)
    # print(f'{len(matches)}')
    # matches = distance_merge(matches, radius=30000, filter_min_len=0)
    # print(f'{len(matches)}')
    # matches = distance_merge(matches, radius=40000, filter_min_len=0)
    # print(f'{len(matches)}')
    # matches = distance_merge(matches, radius=50000, filter_min_len=0)
    # print(f'{len(matches)}')
    # matches = distance_merge(matches, radius=60000, filter_min_len=0)
    # print(f'{len(matches)}')
    # matches = distance_merge(matches, radius=70000, filter_min_len=0)
    # print(f'{len(matches)}')
    # matches = distance_merge(matches, radius=80000, filter_min_len=0)
    # print(f'{len(matches)}')
    # matches = distance_merge(matches, radius=90000, filter_min_len=0)
    # print(f'{len(matches)}')
    # matches = distance_merge(matches, radius=100000, filter_min_len=0)
    # print(f'{len(matches)}')
    # matches = distance_merge(matches, radius=300000, filter_min_len=0)
    # print(f'{len(matches)}')
    # matches = distance_merge(matches, radius=300000, filter_min_len=0)
    # print(f'{len(matches)}')
    # matches = distance_merge(matches, radius=300000, filter_min_len=0)
    # print(f'{len(matches)}')
    plot_raw(matches, y_axis_organism_name='human', x_axis_organism_name='mouse')
    plt.show()