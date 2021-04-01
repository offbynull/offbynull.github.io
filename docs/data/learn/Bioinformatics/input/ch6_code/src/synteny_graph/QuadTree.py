from __future__ import annotations

from random import sample
from typing import Optional, List, Tuple, Set, TypeVar, Dict, Generic

from synteny_graph.GeometryUtils import distance

D = TypeVar('D')


class QuadTree(Generic[D]):
    def __init__(
            self,
            min_x: int,
            max_x: int,
            min_y: int,
            max_y: int,
            parent: Optional[QuadTree] = None,
            subdivision_threshold: int = 8,
            single_points_only: bool = True  # if true, only 1 instance of a single point may exist
    ):
        assert min_x <= max_x
        assert min_y <= max_y
        assert subdivision_threshold > 0
        self.min_x = min_x
        self.min_y = min_y
        self.max_x = max_x
        self.max_y = max_y

        self.points: Optional[Dict[Tuple[int, int], List[D]]] = {}
        self.upperLeft: Optional[QuadTree] = None
        self.upperRight: Optional[QuadTree] = None
        self.lowerLeft: Optional[QuadTree] = None
        self.lowerRight: Optional[QuadTree] = None

        self.parent = parent
        self.subdivision_threshold = subdivision_threshold
        self.single_points_only = single_points_only

    def in_range(self, x: int, y: int) -> bool:
        return self.min_x <= x <= self.max_x and self.min_y <= y <= self.max_y

    def add_point(self, x: int, y: int, data: D) -> None:
        assert self.in_range(x, y)
        if self.points is not None:
            cnt = len(self.points)
            if cnt < self.subdivision_threshold:
                instances = self.points.setdefault((x, y), set())
                if len(instances) > 0 and self.single_points_only:
                    raise ValueError(f'Attempting to insert duplicate point at ({x}, {y})')
                instances.add(data)
            else:
                self._create_branches()
                for (_x, _y), _data_instances in self.points.items():
                    for _data in _data_instances:
                        self._add_to_branch(_x, _y, _data)
                self.points = None
                self._add_to_branch(x, y, data)
        else:
            self._add_to_branch(x, y, data)

    def _add_to_branch(self, x: int, y: int, data: D) -> None:
        if self.upperLeft.in_range(x, y):
            self.upperLeft.add_point(x, y, data)
        elif self.upperRight.in_range(x, y):
            self.upperRight.add_point(x, y, data)
        elif self.lowerLeft.in_range(x, y):
            self.lowerLeft.add_point(x, y, data)
        elif self.lowerRight.in_range(x, y):
            self.lowerRight.add_point(x, y, data)
        else:
            ValueError('???')

    def _create_branches(self) -> None:
        self.upperLeft = QuadTree(
            self.min_x,
            self.min_x + ((self.max_x - self.min_x) // 2),
            self.min_y,
            self.min_y + ((self.max_y - self.min_y) // 2),
            self
        )
        self.upperRight = QuadTree(
            self.min_x + ((self.max_x - self.min_x) // 2) + 1,
            self.max_x,
            self.min_y,
            self.min_y + ((self.max_y - self.min_y) // 2),
            self
        )
        self.lowerLeft = QuadTree(
            self.min_x,
            self.min_x + ((self.max_x - self.min_x) // 2),
            self.min_y + ((self.max_y - self.min_y) // 2) + 1,
            self.max_y,
            self
        )
        self.lowerRight = QuadTree(
            self.min_x + ((self.max_x - self.min_x) // 2) + 1,
            self.max_x,
            self.min_y + ((self.max_y - self.min_y) // 2) + 1,
            self.max_y,
            self
        )

    def remove_point(self, x: int, y: int, data: D) -> None:
        assert self.in_range(x, y)
        if self.points is not None:
            pt = (x, y)
            if pt not in self.points:
                raise ValueError(f'No point at ({x}, {y})')
            instances = self.points[pt]
            if data not in instances:
                raise ValueError(f'Data does not exist at point ({x}, {y})')
            instances.remove(data)
            if not instances:
                del self.points[pt]
        else:
            self._remove_from_branch(x, y, data)
        if self.points is None:
            self._destroy_branches()  # THIS CELL AND SOME OF ITS PARENTS MAY BE REMOVED FROM TREE AFTER THIS

    def _remove_from_branch(self, x: int, y: int, data: D) -> None:
        if self.upperLeft.in_range(x, y):
            self.upperLeft.remove_point(x, y, data)
        elif self.upperRight.in_range(x, y):
            self.upperRight.remove_point(x, y, data)
        elif self.lowerLeft.in_range(x, y):
            self.lowerLeft.remove_point(x, y, data)
        elif self.lowerRight.in_range(x, y):
            self.lowerRight.remove_point(x, y, data)
        else:
            ValueError('???')

    def _destroy_branches(self) -> None:
        if self.upperLeft.points is not None and len(self.upperLeft.points) == 0\
                and self.upperRight.points is not None and len(self.upperRight.points) == 0\
                and self.lowerLeft.points is not None and len(self.lowerLeft.points) == 0\
                and self.lowerRight.points is not None and len(self.lowerRight.points) == 0:
            self.upperLeft = None
            self.upperRight = None
            self.lowerLeft = None
            self.lowerRight = None
            self.points = {}

    def get_points(self) -> Set[Tuple[int, int, D]]:
        if self.points is not None:
            ret = set()
            for (x1, x2), data_instances in self.points.items():
                for data in data_instances:
                    ret.add((x1, x2, data))
            return ret
        return self.upperLeft.get_points() | self.upperRight.get_points() | self.lowerLeft.get_points() | self.lowerRight.get_points()

    def get_points_within_radius(self, x: int, y: int, radius: int) -> Set[Tuple[int, int, D]]:
        cells = self._find_confining_cells(
            max(x - radius, self.min_x),
            min(x + radius, self.max_x),
            max(y - radius, self.min_y),
            min(y + radius, self.max_y)
        )
        ret = set()
        for cell in cells:
            for point in cell.get_points():
                if distance(point[0], x, point[1], y) <= radius:
                    ret.add(point)
        return ret

    def is_empty(self):
        if self.points is None:
            return False
        elif self.points is not None and len(self.points) == 0:
            return True
        else:
            return False

    def _find_confining_cells(self, min_x: int, max_x: int, min_y: int, max_y: int) -> List[QuadTree]:
        assert min_x >= self.min_x and max_x <= self.max_x, "X is OOB"
        assert min_y >= self.min_y and max_y <= self.max_y, "Y is OOB"
        found_cells = []
        cell_row = []
        next_x = min_x
        next_y = min_y
        while next_y <= max_y:
            while next_x <= max_x:
                found_qt = self._walk_to_branch_containing(next_x, next_y)
                cell_row.append(found_qt)
                next_x = found_qt.max_x + 1
            next_x = min_x
            next_y = min(qt.max_y for qt in cell_row) + 1
            found_cells += cell_row
            cell_row = []
        return found_cells

    def _walk_to_branch_containing(self, x: int, y: int) -> QuadTree:
        if self.points is not None:
            return self
        if self.upperLeft.in_range(x, y):
            return self.upperLeft._walk_to_branch_containing(x, y)
        elif self.upperRight.in_range(x, y):
            return self.upperRight._walk_to_branch_containing(x, y)
        elif self.lowerLeft.in_range(x, y):
            return self.lowerLeft._walk_to_branch_containing(x, y)
        elif self.lowerRight.in_range(x, y):
            return self.lowerRight._walk_to_branch_containing(x, y)
        else:
            raise ValueError('???')


if __name__ == '__main__':
    qt = QuadTree(0, 1000, 0, 1000, subdivision_threshold=4)


    for x, y in zip(sample(range(0, 1000), 1000), sample(range(0, 1000), 1000)):
        qt.add_point(x, y, '')

    expected = set()
    for p in qt.get_points():
        if distance(p[0], 500, p[1], 500) <= 50:
            expected.add(p)
    actual = set()
    for p in qt.get_points_within_radius(500, 500, 50):
        actual.add(p)
    print(f'{expected}')
    print(f'{actual}')
    print(f'{expected == actual}')


    for p in qt.get_points():
        qt.remove_point(p[0], p[1], p[2])

    expected = set()
    for p in qt.get_points():
        if distance(p[0], 500, p[1], 500) <= 50:
            expected.add(p)
    actual = set()
    for p in qt.get_points_within_radius(500, 500, 50):
        actual.add(p)
    print(f'{expected}')
    print(f'{actual}')
    print(f'{expected == actual}')