from typing import List, Any, Optional, TypeVar

from GraphGridCreate import create_grid_graph
from WeightLookup import WeightLookup, Constant2DWeightLookup

ELEM = TypeVar('ELEM')

class NodeData:
    def __init__(self):
        ...

class EdgeData:
    def __init__(self, v_elem: ELEM, w_elem: ELEM, weight: float):
        self.v_elem = v_elem
        self.w_elem = w_elem

def global_alignment(v: List[ELEM], w: List[ELEM], weight_lookup: WeightLookup, buffer: Optional[List[List[Any]]] = None):
    v_node_count = len(v) + 1
    w_node_count = len(w) + 1
    create_grid_graph(
        [list(v), list(w)],
        lambda n_id: (True, NodeData()),
        lambda src_n_id, dst_n_id, offset, elems: (True, EdgeData(elems[0], elems[1], weight_lookup.lookup(elems)))
        on_new_node: Optional[
            Callable[
                [
                    Tuple[int, ...]  # node id / coord
                ],
                Tuple[bool, Optional[ND]]  # flag indicating if node could be added, node data
            ]
        ] = None,
        on_new_edge: Optional[
            Callable[
                [
                    Tuple[int, ...],  # src node id / coord
                    Tuple[int, ...],  # dst node id / coord
                    Tuple[int, ...],  # coord offsets (same as dst coord - src coord)
                    Tuple[Optional[ELEM], ...]   # sequence elements at each coord
                ],
                Tuple[bool, Optional[ED]]  # flag indicating if edge could be added, edge data
            ]
        ] = None)
    if buffer is None:
        buffer = []
        for v_idx in range(v_node_count):
            row = []
            for w_idx in range(w_node_count):
                row.append([-1, None])
            buffer.append(row)
    for v_idx in range(v_node_count):
        buffer[v_idx][0][0] = 0
    for w_idx in range(w_node_count):
        buffer[0][w_idx][0] = 0
    for v_idx in range(1, v_node_count):
        for w_idx in range(1, w_node_count):
            buffer[v_idx][w_idx] = max(
                (buffer[v_idx - 1][w_idx][0] + weight_lookup.lookup(v[v_idx - 1], None), '↓'),
                (buffer[v_idx][w_idx - 1][0] + weight_lookup.lookup(None, w[w_idx - 1]), '→'),
                (buffer[v_idx - 1][w_idx - 1][0] + weight_lookup.lookup(v[v_idx - 1], w[w_idx - 1]), '↘'),
                key=lambda x: x[0]
            )
    return buffer


s1 = 'STEAK'
s2 = 'BREAK'
matrix = global_alignment('STEAK', 'BREAK', Constant2DWeightLookup(1, 0, 0))


import sys
sys.setrecursionlimit(2000)
out = output_lcs(matrix, s1, len(s1), len(s2))
print(f'{out}')