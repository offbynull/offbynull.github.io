from typing import Dict, List, Tuple, Set

from helpers.GeometryUtils import angle, distance, test_angle_between, normalize_degree
from synteny_graph.Match import Match, MatchType
from synteny_graph.QuadTree import QuadTree


class MatchSpatialIndexer:
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

    def scan(self, match: Match, search_radius: int, search_angle_half_maw: int = 45) -> Set[Match]:
        assert search_radius > 0
        assert 0 <= search_angle_half_maw < 180
        found = {match}
        if match.type == MatchType.NORMAL:
            self._scan_norm_to_end(match, search_radius, search_angle_half_maw, found)
            self._scan_norm_to_start(match, search_radius, search_angle_half_maw, found)
        elif match.type == MatchType.REVERSE_COMPLEMENT:
            self._scan_rc_to_end(match, search_radius, search_angle_half_maw, found)
            self._scan_rc_to_start(match, search_radius, search_angle_half_maw, found)
        else:
            raise ValueError('???')
        return found

    @staticmethod
    def _find_potential_matches(
            quadtree: QuadTree[Match],
            center_x: int,
            center_y: int,
            radius: int,
            angel_start: float,
            angle_end: float
    ):
        quadtree_matches = quadtree.get_points_within_radius(center_x, center_y, radius)
        final_matches = set()
        for x, y, match in quadtree_matches:
            exact_match = x == center_x and y == center_y
            if exact_match:
                allowed = True
            else:
                _angle = angle(center_x, x, center_y, y)
                allowed = test_angle_between(_angle, angel_start, angle_end)
            if allowed:
                dist = distance(center_x, x, center_y, y)
                final_matches.add((match, dist))
        return final_matches

    def _scan_norm_to_end(self, match: Match, radius: int, angle_maw: int, found: Set[Match]):
        assert match.type == MatchType.NORMAL
        angle_start = normalize_degree(45 - angle_maw)
        angle_end = normalize_degree(45 + angle_maw)
        x, y = match.get_end_point()
        chr_pair = match.x_axis_chromosome, match.y_axis_chromosome
        quadtree = self.norm_start_quadtrees[chr_pair]
        while True:
            potential_matches = MatchSpatialIndexer._find_potential_matches(
                quadtree,
                x, y,
                radius,
                angle_start, angle_end
            )
            potential_matches = {(m, d) for m, d in potential_matches if m not in found}  # remove if already in found
            if not potential_matches:
                break
            found_match = min(potential_matches, key=lambda x: x[1])
            x, y = found_match[0].get_end_point()
            found.add(found_match[0])

    def _scan_norm_to_start(self, match: Match, radius: int, angle_maw: int, found: Set[Match]):
        assert match.type == MatchType.NORMAL
        angle_start = normalize_degree(225 - angle_maw)
        angle_end = normalize_degree(225 + angle_maw)
        x, y = match.get_start_point()
        chr_pair = match.x_axis_chromosome, match.y_axis_chromosome
        quadtree = self.norm_end_quadtrees[chr_pair]
        while True:
            potential_matches = MatchSpatialIndexer._find_potential_matches(
                quadtree,
                x, y,
                radius,
                angle_start, angle_end
            )
            potential_matches = {(m, d) for m, d in potential_matches if m not in found}  # remove if already in found
            if not potential_matches:
                break
            found_match = min(potential_matches, key=lambda x: x[1])
            x, y = found_match[0].get_start_point()
            found.add(found_match[0])

    def _scan_rc_to_end(self, match: Match, radius: int, angle_maw: int, found: Set[Match]):
        assert match.type == MatchType.REVERSE_COMPLEMENT
        angle_start = normalize_degree(315 - angle_maw)
        angle_end = normalize_degree(315 + angle_maw)
        x, y = match.get_end_point()
        chr_pair = match.x_axis_chromosome, match.y_axis_chromosome
        quadtree = self.rc_start_quadtrees[chr_pair]
        while True:
            potential_matches = MatchSpatialIndexer._find_potential_matches(
                quadtree,
                x, y,
                radius,
                angle_start, angle_end
            )
            potential_matches = {(m, d) for m, d in potential_matches if m not in found}  # remove if already in found
            if not potential_matches:
                break
            found_match = min(potential_matches, key=lambda x: x[1])
            x, y = found_match[0].get_end_point()
            found.add(found_match[0])

    def _scan_rc_to_start(self, match: Match, radius: int, angle_maw: int, found: Set[Match]):
        assert match.type == MatchType.REVERSE_COMPLEMENT
        angle_start = normalize_degree(135 - angle_maw)
        angle_end = normalize_degree(135 + angle_maw)
        x, y = match.get_start_point()
        chr_pair = match.x_axis_chromosome, match.y_axis_chromosome
        quadtree = self.rc_end_quadtrees[chr_pair]
        while True:
            potential_matches = MatchSpatialIndexer._find_potential_matches(
                quadtree,
                x, y,
                radius,
                angle_start, angle_end
            )
            potential_matches = {(m, d) for m, d in potential_matches if m not in found}  # remove if already in found
            if not potential_matches:
                break
            found_match = min(potential_matches, key=lambda x: x[1])
            x, y = found_match[0].get_start_point()
            found.add(found_match[0])
