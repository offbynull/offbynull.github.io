from __future__ import annotations

import colorsys
import lzma
import random
from enum import Enum
from math import sqrt, ceil
from typing import Iterable, Set, Dict, Optional, List

import matplotlib.collections as mc
import matplotlib.pyplot as plt
import pylab as pl

from synteny_graph.GeometryUtils import distance, slope
from synteny_graph.Match import Match, MatchType
from synteny_graph.QuadTree import QuadTree


class Direction(Enum):
    FORWARD = 'FORWARD'
    BACKWARD = 'BACKWARD'


def _find_potential_matches(
        quadtree: QuadTree[Match],
        remaining: Set[Match],
        x_axis_chromosome: str,
        y_axis_chromosome: str,
        center_x: int,
        center_y: int,
        radius: int,
        slope1: float,
        slope2: float,
        type: MatchType,
        direction: Direction
):
    slope1, slope2 = sorted([slope1, slope2])
    quadtree_matches = quadtree.get_points_within_radius(center_x, center_y, radius)
    final_matches = set()
    for x, y, match in quadtree_matches:
        if match.type != type or match.x_axis_chromosome != x_axis_chromosome or match.y_axis_chromosome != y_axis_chromosome or match not in remaining:
            continue
        if direction == Direction.FORWARD:
            if x >= center_x:
                _slope = slope(center_x, x, center_y, y)
            else:
                continue
        elif direction == Direction.BACKWARD:
            if x <= center_x:
                _slope = slope(center_x, x, y, center_y)
            else:
                continue
        else:
            raise ValueError('???')
        if slope1 <= _slope <= slope2:
            dist = distance(center_x, x, center_y, y)
            final_matches.add((match, dist))
    return final_matches


def _scan_norm_to_end(starting_match: Match, remaining: Set[Match], norm_start_quadtree: QuadTree[Match], radius: int, chain: List[Match]):
    assert starting_match.type == MatchType.NORMAL
    assert starting_match in remaining
    end_x, end_y = starting_match.get_end_point()
    while True:
        potential_matches = _find_potential_matches(norm_start_quadtree, remaining, starting_match.x_axis_chromosome, starting_match.y_axis_chromosome, end_x, end_y, radius, 0.1, 1.0, MatchType.NORMAL, Direction.FORWARD)
        if not potential_matches:
            break
        found_match = min(potential_matches, key=lambda x: x[1])
        end_x, end_y = found_match[0].get_end_point()
        chain.append(found_match[0])


def _scan_norm_to_start(starting_match: Match, remaining: Set[Match], norm_end_quadtree: QuadTree[Match], radius: int, chain: List[Match]):
    assert starting_match.type == MatchType.NORMAL
    assert starting_match in remaining
    start_x, start_y = starting_match.get_start_point()
    temp_chain = []
    while True:
        potential_matches = _find_potential_matches(norm_end_quadtree, remaining, starting_match.x_axis_chromosome, starting_match.y_axis_chromosome, start_x, start_y, radius, 0.1, 1.0, MatchType.NORMAL, Direction.BACKWARD)
        if not potential_matches:
            break
        found_match = min(potential_matches, key=lambda x: x[1])
        start_x, start_y = found_match[0].get_start_point()
        temp_chain.append(found_match[0])
    chain[0:0] = temp_chain[::-1]


def _scan_rc_to_end(starting_match: Match, remaining: Set[Match], rc_start_quadtree: QuadTree[Match], radius: int, chain: List[Match]):
    assert starting_match.type == MatchType.REVERSE_COMPLEMENT
    assert starting_match in remaining
    end_x, end_y = starting_match.get_end_point()
    while remaining:
        potential_matches = _find_potential_matches(rc_start_quadtree, remaining, starting_match.x_axis_chromosome, starting_match.y_axis_chromosome, end_x, end_y, radius, -0.1, -1.0, MatchType.REVERSE_COMPLEMENT, Direction.FORWARD)
        if not potential_matches:
            break
        found_match = min(potential_matches, key=lambda x: x[1])
        end_x, end_y = found_match[0].get_end_point()
        chain.append(found_match[0])


def _scan_rc_to_start(starting_match: Match, remaining: Set[Match], rc_end_quadtree: QuadTree[Match], radius: int, chain: List[Match]):
    assert starting_match.type == MatchType.REVERSE_COMPLEMENT
    assert starting_match in remaining
    start_x, start_y = starting_match.get_start_point()
    temp_chain = []
    while True:
        potential_matches = _find_potential_matches(rc_end_quadtree, remaining, starting_match.x_axis_chromosome, starting_match.y_axis_chromosome, start_x, start_y, radius, -0.1, -1.0, MatchType.REVERSE_COMPLEMENT, Direction.BACKWARD)
        if not potential_matches:
            break
        found_match = min(potential_matches, key=lambda x: x[1])
        start_x, start_y = found_match[0].get_start_point()
        temp_chain.append(found_match[0])
    chain[0:0] = temp_chain[::-1]


def identify_synteny_blocks(matches: Iterable[Match], radius: int, synteny_min_len: int):
    min_x = min(m.x_axis_chromosome_min_idx for m in matches)
    max_x = max(m.x_axis_chromosome_max_idx for m in matches)
    min_y = min(m.y_axis_chromosome_min_idx for m in matches)
    max_y = max(m.y_axis_chromosome_max_idx for m in matches)
    y_axis_chromosomes: Set[str] = {m.y_axis_chromosome for m in matches}
    norm_start_quadtrees: Dict[str, QuadTree] = {chromosome: QuadTree(min_x, max_x, min_y, max_y) for chromosome in y_axis_chromosomes}
    norm_end_quadtrees: Dict[str, QuadTree] = {chromosome: QuadTree(min_x, max_x, min_y, max_y) for chromosome in y_axis_chromosomes}
    rc_start_quadtrees: Dict[str, QuadTree] = {chromosome: QuadTree(min_x, max_x, min_y, max_y) for chromosome in y_axis_chromosomes}
    rc_end_quadtrees: Dict[str, QuadTree] = {chromosome: QuadTree(min_x, max_x, min_y, max_y) for chromosome in y_axis_chromosomes}
    for m in matches:
        start_pt = m.get_start_point() + (m,)
        end_pt = m.get_end_point() + (m,)
        if m.type == MatchType.NORMAL:
            norm_start_quadtrees[m.y_axis_chromosome].add_point(*start_pt)
            norm_end_quadtrees[m.y_axis_chromosome].add_point(*end_pt)
        elif m.type == MatchType.REVERSE_COMPLEMENT:
            rc_start_quadtrees[m.y_axis_chromosome].add_point(*start_pt)
            rc_end_quadtrees[m.y_axis_chromosome].add_point(*end_pt)
        else:
            raise ValueError('???')

    ret = []
    for y_axis_chromosome in y_axis_chromosomes:
        norm_start_quadtree = norm_start_quadtrees[y_axis_chromosome]
        norm_end_quadtree = norm_end_quadtrees[y_axis_chromosome]
        rc_start_quadtree = rc_start_quadtrees[y_axis_chromosome]
        rc_end_quadtree = rc_end_quadtrees[y_axis_chromosome]
        remaining = {m for m in matches if m.y_axis_chromosome == y_axis_chromosome}
        while remaining:
            m = next(iter(remaining))
            if m.type == MatchType.NORMAL:
                end_chain: List[Match] = []
                start_chain: List[Match] = []
                _scan_norm_to_end(m, remaining, norm_start_quadtree, radius, end_chain)
                _scan_norm_to_start(m, remaining, norm_end_quadtree, radius, start_chain)
            elif m.type == MatchType.REVERSE_COMPLEMENT:
                end_chain: List[Match] = []
                start_chain: List[Match] = []
                _scan_rc_to_end(m, remaining, rc_start_quadtree, radius, end_chain)
                _scan_rc_to_start(m, remaining, rc_end_quadtree, radius, start_chain)
            else:
                raise ValueError('???')
            chain = start_chain + [m] + end_chain
            chain_start_pt = chain[0].get_start_point()
            chain_end_pt = chain[-1].get_end_point()
            chain_dist = distance(chain_end_pt[0], chain_start_pt[0], chain_end_pt[1], chain_start_pt[1])
            if chain_dist >= synteny_min_len:
                remaining.difference_update(chain)
                merged_m = Match.merge(chain)
                ret.append(merged_m)
            else:
                remaining.remove(m)
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

    # matches = random.sample(matches, len(matches) // 4)
    matches = identify_synteny_blocks(matches, radius=50000, synteny_min_len=50000 * 15)

    plot_raw(matches, y_axis_organism_name='human', x_axis_organism_name='mouse')
    plt.show()