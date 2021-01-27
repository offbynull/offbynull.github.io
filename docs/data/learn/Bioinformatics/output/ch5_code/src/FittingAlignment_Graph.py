from abc import ABC, abstractmethod
from typing import List, Optional, TypeVar, Tuple

from Backtrack import backtrack
from Graph import Graph
from GraphGridCreate import create_grid_graph
from FindMaxPath_DPBacktrack import populate_weights_and_backtrack_pointers
from WeightLookup import WeightLookup, Constant2DWeightLookup
from helpers.Utils import unique_id_generator

ELEM = TypeVar('ELEM')
N = TypeVar('N')
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


class EdgeData(ABC):
    def __init__(self, weight: float):
        self.weight = weight

    @abstractmethod
    def get_elements(self) -> Tuple[Optional[ELEM], Optional[ELEM]]:
        ...


class StandardEdgeData(EdgeData):
    def __init__(self, v_elem: Optional[ELEM], w_elem: Optional[ELEM], weight: float):
        super().__init__(weight)
        self.v_elem = v_elem
        self.w_elem = w_elem

    def get_elements(self) -> Tuple[Optional[ELEM], Optional[ELEM]]:
        return self.v_elem, self.w_elem


class FreeRideEdgeData(EdgeData):
    def __init__(self):
        super().__init__(0.0)

    def get_elements(self) -> Tuple[Optional[ELEM], Optional[ELEM]]:
        raise AttributeError('No elements on free-rides')


def fitting_alignment(v: List[ELEM], w: List[ELEM], weight_lookup: WeightLookup) -> Tuple[float, List[List[ELEM]]]:
    v_node_count = len(v) + 1
    w_node_count = len(w) + 1
    # generate grid graph
    graph: Graph[Tuple[int, ...], NodeData, str, EdgeData] = create_grid_graph(
        [v, w],
        lambda n_id: NodeData(),
        lambda src_n_id, dst_n_id, offset, elems: StandardEdgeData(elems[0], elems[1], weight_lookup.lookup(*elems))
    )
    # add free rides from source node
    from_node = (0, 0)
    src_free_ride_id_create_func = unique_id_generator('SRC_FREE_RIDE')
    for v_idx in range(1, v_node_count):
        graph.insert_edge(
            src_free_ride_id_create_func(),
            from_node,
            (v_idx, 0),
            FreeRideEdgeData()
        )
    # add free rides to sink node
    to_node = (v_node_count - 1, w_node_count - 1)
    sink_free_ride_id_create_func = unique_id_generator('SINK_FREE_RIDE')
    for v_idx in range(0, v_node_count - 1):
        graph.insert_edge(
            sink_free_ride_id_create_func(),
            (v_idx, w_node_count - 1),
            to_node,
            FreeRideEdgeData()
        )
    # populate backtrack pointers
    populate_weights_and_backtrack_pointers(
        graph,
        from_node,
        lambda n_id, weight, e_id: graph.get_node_data(n_id).set_weight_and_backtracking_edge(weight, e_id),
        lambda n_id: graph.get_node_data(n_id).get_weight_and_backtracking_edge(),
        lambda e_id: graph.get_edge_data(e_id).weight
    )
    # pull out results
    final_weight = graph.get_node_data(to_node).weight
    alignment = backtrack(
        graph,
        to_node,
        lambda n_id: graph.get_node_data(n_id).get_weight_and_backtracking_edge(),
        lambda e_id: graph.get_edge_data(e_id).get_elements(),
        lambda e_id: isinstance(graph.get_edge_data(e_id), FreeRideEdgeData)
    )
    return final_weight, alignment


if __name__ == '__main__':
    s1 = list('GTAGGCTTAAGGTTA')
    s2 = list('TAGATA')
    final_score, alignment = fitting_alignment(s1, s2, Constant2DWeightLookup(1, -1, -1))
    print(final_score)
    for alignment_string in alignment:
        for ch in alignment_string:
            print(f'{"-" if ch is None else ch}', end='')
        print()