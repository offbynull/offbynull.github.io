from typing import TypeVar, List, Tuple

from Global_ForwardSweeper import ForwardSweeper
from Global_ReverseSweeper import ReverseSweeper
from WeightLookup import WeightLookup

ELEM = TypeVar('ELEM')


class SweepCombiner:
    def __init__(self, v: List[ELEM], w: List[ELEM], weight_lookup: WeightLookup):
        self.forward_sweeper = ForwardSweeper(v, w, weight_lookup)
        self.reverse_sweeper = ReverseSweeper(v, w, weight_lookup)

    def get_col(self, idx: int):
        fcol = self.forward_sweeper.get_col(idx)
        rcol = self.reverse_sweeper.get_col(idx)
        return [a + b for a, b in zip(fcol, rcol)]


def find_alignment_path_column_edge(v: List[ELEM], w: List[ELEM], col: int, weight_lookup: WeightLookup) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    sc = SweepCombiner(v, w, weight_lookup)
    converged_weights_col = sc.get_col(col)
    converged_weights_next_col = sc.get_col(col + 1)
    max_row_idx, _ = max(enumerate(converged_weights_col), key=lambda x: x[1])
    v_node_count = len(v) + 1
    w_node_count = len(w) + 1
    neighbours = []
    if col + 1 < w_node_count:
        neighbours += [(converged_weights_next_col[max_row_idx], (max_row_idx, max_row_idx + 1))]
    if max_row_idx + 1 < v_node_count and max_row_idx < w_node_count:
        neighbours += [(converged_weights_next_col[max_row_idx + 1], (max_row_idx + 1, max_row_idx + 1))]
    if max_row_idx + 1 < v_node_count:
        neighbours += [(converged_weights_col[max_row_idx + 1], (max_row_idx + 1, max_row_idx))]
    _, (next_row, next_col) = max( neighbours, key=lambda x: x[0])
    return (max_row_idx, max_row_idx), (next_row, next_col)
