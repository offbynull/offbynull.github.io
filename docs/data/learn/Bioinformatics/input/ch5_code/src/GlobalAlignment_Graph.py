from typing import List, Any, Optional, TypeVar

from Backtrack import backtrack
from GraphGridCreate import create_grid_graph
from PopulateWeightsAndBacktrackPointers_DynamicProgramming import populate_weights_and_backtrack_pointers
from WeightLookup import WeightLookup, Constant2DWeightLookup

ELEM = TypeVar('ELEM')
E = TypeVar('E')

class NodeData:
    def __init__(self):
        self.weight = None
        self.backtracking_edge = None

    def set_weight_and_backtracking_edge(self, weight: float, backtracking_edge: E):
        self.weight = weight
        self.backtracking_edge = backtracking_edge

    def get_weight_and_backtracking_edge(self):
        return self.weight, self.backtracking_edge

class EdgeData:
    def __init__(self, v_elem: ELEM, w_elem: ELEM, weight: float):
        self.v_elem = v_elem
        self.w_elem = w_elem
        self.weight = weight

    def get_elements(self):
        return self.v_elem, self.w_elem

def global_alignment(v: List[ELEM], w: List[ELEM], weight_lookup: WeightLookup):
    v_node_count = len(v) + 1
    w_node_count = len(w) + 1
    graph = create_grid_graph(
        [v, w],
        lambda n_id: (True, NodeData()),
        lambda src_n_id, dst_n_id, offset, elems: (True, EdgeData(elems[0], elems[1], weight_lookup.lookup(*elems)))
    )
    from_node = (0, 0)
    to_node = (v_node_count - 1, w_node_count - 1)
    populate_weights_and_backtrack_pointers(
        graph,
        from_node,
        lambda n_id, weight, e_id: graph.get_node_data(n_id).set_weight_and_backtracking_edge(weight, e_id),
        lambda n_id: graph.get_node_data(n_id).get_weight_and_backtracking_edge(),
        lambda e_id: graph.get_edge_data(e_id).weight
    )
    alignments = backtrack(
        graph,
        to_node,
        lambda n_id: graph.get_node_data(n_id).get_weight_and_backtracking_edge(),
        lambda e_id: graph.get_edge_data(e_id).get_elements()
    )
    return alignments


if __name__ == '__main__':
    s1 = list('STEAK')
    s2 = list('BREAK')
    alignment = global_alignment(s1, s2, Constant2DWeightLookup(1, 0, 0))
    for a in alignment:
        print(f'{a}')