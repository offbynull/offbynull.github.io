from typing import Dict, List, Tuple

from synteny_graph.GeometryUtils import angle, distance
from synteny_graph.Match import Match, MatchType
from synteny_graph.QuadTree import QuadTree


class MatchIndexer:
    def __init__(self, min_x: int, max_x: int, min_y: int, max_y: int):
        assert min_x <= max_x
        assert min_y <= max_y
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y
        self.norm_start_quadtrees: Dict[Tuple[str, str], QuadTree] = {}
        self.norm_end_quadtrees: Dict[Tuple[str, str], QuadTree] = {}
        self.rc_start_quadtrees: Dict[Tuple[str, str], QuadTree] = {}
        self.rc_end_quadtrees: Dict[Tuple[str, str], QuadTree] = {}

    def index(self, match: Match):
        chromosome_pair = match.x_axis_chromosome, match.y_axis_chromosome
        start_pt = match.get_start_point() + (match,)
        end_pt = match.get_end_point() + (match,)
        if match.type == MatchType.NORMAL:
            self.norm_start_quadtrees.setdefault(chromosome_pair, QuadTree(self.min_x, self.max_x, self.min_y, self.max_y)).add_point(*start_pt)
            self.norm_end_quadtrees.setdefault(chromosome_pair, QuadTree(self.min_x, self.max_x, self.min_y, self.max_y)).add_point(*end_pt)
        elif match.type == MatchType.REVERSE_COMPLEMENT:
            self.rc_start_quadtrees.setdefault(chromosome_pair, QuadTree(self.min_x, self.max_x, self.min_y, self.max_y)).add_point(*start_pt)
            self.rc_end_quadtrees.setdefault(chromosome_pair, QuadTree(self.min_x, self.max_x, self.min_y, self.max_y)).add_point(*end_pt)
        else:
            raise ValueError('???')

    def unindex(self, match: Match):
        chromosome_pair = match.x_axis_chromosome, match.y_axis_chromosome
        start_pt = match.get_start_point() + (match,)
        end_pt = match.get_end_point() + (match,)
        if match.type == MatchType.NORMAL:
            self.norm_start_quadtrees[chromosome_pair].remove_point(*start_pt)
            self.norm_end_quadtrees[chromosome_pair].remove_point(*end_pt)
            if self.norm_start_quadtrees[chromosome_pair].is_empty():
                del self.norm_start_quadtrees[chromosome_pair]
            if self.norm_end_quadtrees[chromosome_pair].is_empty():
                del self.norm_end_quadtrees[chromosome_pair]
        elif match.type == MatchType.REVERSE_COMPLEMENT:
            self.rc_start_quadtrees[chromosome_pair].remove_point(*start_pt)
            self.rc_end_quadtrees[chromosome_pair].remove_point(*end_pt)
            if self.rc_start_quadtrees[chromosome_pair].is_empty():
                del self.rc_start_quadtrees[chromosome_pair]
            if self.rc_end_quadtrees[chromosome_pair].is_empty():
                del self.rc_end_quadtrees[chromosome_pair]
        else:
            raise ValueError('???')

    def scan(self, match: Match, radius: int):
        if match.type == MatchType.NORMAL:
            end_chain: List[Match] = []
            start_chain: List[Match] = []
            self._scan_norm_to_end(match, radius, end_chain)
            self._scan_norm_to_start(match, radius, start_chain)
        elif match.type == MatchType.REVERSE_COMPLEMENT:
            end_chain: List[Match] = []
            start_chain: List[Match] = []
            self._scan_rc_to_end(match, radius, end_chain)
            self._scan_rc_to_start(match, radius, start_chain)
        else:
            raise ValueError('???')
        return start_chain + [match] + end_chain

    @staticmethod
    def _find_potential_matches(
            quadtree: QuadTree[Match],
            center_x: int,
            center_y: int,
            radius: int,
            min_degree: float,
            max_degree: float
    ):
        quadtree_matches = quadtree.get_points_within_radius(center_x, center_y, radius)
        final_matches = set()
        for x, y, match in quadtree_matches:
            degree = angle(center_x, x, center_y, y)
            if min_degree <= degree <= max_degree:
                dist = distance(center_x, x, center_y, y)
                final_matches.add((match, dist))
        return final_matches


    def _scan_norm_to_end(self, match: Match, radius: int, chain: List[Match]):
        assert match.type == MatchType.NORMAL
        x, y = match.get_end_point()
        chr_pair = match.x_axis_chromosome, match.y_axis_chromosome
        quadtree = self.norm_start_quadtrees[chr_pair]
        while True:
            potential_matches = MatchIndexer._find_potential_matches(
                quadtree,
                x, y,
                radius,
                10, 80
            )
            if not potential_matches:
                break
            found_match = min(potential_matches, key=lambda x: x[1])
            x, y = found_match[0].get_end_point()
            chain.append(found_match[0])


    def _scan_norm_to_start(self, match: Match, radius: int, chain: List[Match]):
        assert match.type == MatchType.NORMAL
        x, y = match.get_start_point()
        chr_pair = match.x_axis_chromosome, match.y_axis_chromosome
        quadtree = self.norm_end_quadtrees[chr_pair]
        temp_chain = []
        while True:
            potential_matches = MatchIndexer._find_potential_matches(
                quadtree,
                x, y,
                radius,
                190, 260
            )
            if not potential_matches:
                break
            found_match = min(potential_matches, key=lambda x: x[1])
            x, y = found_match[0].get_start_point()
            temp_chain.append(found_match[0])
        chain[0:0] = temp_chain[::-1]


    def _scan_rc_to_end(self, match: Match, radius: int, chain: List[Match]):
        assert match.type == MatchType.REVERSE_COMPLEMENT
        x, y = match.get_end_point()
        chr_pair = match.x_axis_chromosome, match.y_axis_chromosome
        quadtree = self.rc_start_quadtrees[chr_pair]
        while True:
            potential_matches = MatchIndexer._find_potential_matches(
                quadtree,
                x, y,
                radius,
                280, 350
            )
            if not potential_matches:
                break
            found_match = min(potential_matches, key=lambda x: x[1])
            x, y = found_match[0].get_end_point()
            chain.append(found_match[0])


    def _scan_rc_to_start(self, match: Match, radius: int, chain: List[Match]):
        assert match.type == MatchType.REVERSE_COMPLEMENT
        x, y = match.get_start_point()
        chr_pair = match.x_axis_chromosome, match.y_axis_chromosome
        quadtree = self.rc_end_quadtrees[chr_pair]
        temp_chain = []
        while True:
            potential_matches = MatchIndexer._find_potential_matches(
                quadtree,
                x, y,
                radius,
                100, 170
            )
            if not potential_matches:
                break
            found_match = min(potential_matches, key=lambda x: x[1])
            x, y = found_match[0].get_start_point()
            temp_chain.append(found_match[0])
        chain[0:0] = temp_chain[::-1]