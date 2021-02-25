from typing import List, Optional, TypeVar, Tuple

from WeightLookup import WeightLookup, Table2DWeightLookup
from find_max_path.FindMaxPath_DPBacktrack import populate_weights_and_backtrack_pointers, backtrack
from graph.Graph import Graph
from graph.GraphGridCreate import create_grid_graph

ELEM = TypeVar('ELEM')

class NodeData:
    def __init__(self):
        self.weight = None
        self.backtracking_edge = None

    def set_weight_and_backtracking_edge(self, weight: float, backtracking_edge: str):
        self.weight = weight
        self.backtracking_edge = backtracking_edge

    def get_weight_and_backtracking_edge(self):
        return self.weight, self.backtracking_edge


class EdgeData:
    def __init__(self, v_elem: Optional[ELEM], w_elem: Optional[ELEM], weight: float):
        self.v_elem = v_elem
        self.w_elem = w_elem
        self.weight = weight

    def get_elements(self) -> Tuple[Optional[ELEM], Optional[ELEM]]:
        return self.v_elem, self.w_elem


# MARKDOWN
def create_global_alignment_graph(
        seqs: List[List[ELEM]],
        weight_lookup: WeightLookup
) -> Graph[Tuple[int, ...], NodeData, str, EdgeData]:
    graph = create_grid_graph(
        seqs,
        lambda n_id: NodeData(),
        lambda src_n_id, dst_n_id, offset, elems: EdgeData(elems[0], elems[1], weight_lookup.lookup(*elems))
    )
    return graph


def global_alignment(
        seqs: List[List[ELEM]],
        weight_lookup: WeightLookup
) -> Tuple[float, List[str], List[Tuple[ELEM, ...]]]:
    seq_node_counts = [len(s) + 1 for s in seqs]
    graph = create_global_alignment_graph(seqs, weight_lookup)
    from_node = tuple([0] * len(seqs))
    to_node = tuple(seq_node_counts)
    populate_weights_and_backtrack_pointers(
        graph,
        from_node,
        lambda n_id, weight, e_id: graph.get_node_data(n_id).set_weight_and_backtracking_edge(weight, e_id),
        lambda n_id: graph.get_node_data(n_id).get_weight_and_backtracking_edge(),
        lambda e_id: graph.get_edge_data(e_id).weight
    )
    final_weight = graph.get_node_data(to_node).weight
    edges = backtrack(
        graph,
        to_node,
        lambda n_id: graph.get_node_data(n_id).get_weight_and_backtracking_edge()
    )
    alignment = []
    for e in edges:
        ed = graph.get_edge_data(e)
        alignment.append((ed.v_elem, ed.w_elem))
    return final_weight, edges, alignment
# MARKDOWN


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        dims = int(input())
        seqs = [list(input()) for _ in range(dims)]
        FIX ME: MATRIX TYPE IS 3D
        FIX ME: MATRIX TYPE IS 3D
        FIX ME: MATRIX TYPE IS 3D
        FIX ME: MATRIX TYPE IS 3D
        FIX ME: MATRIX TYPE IS 3D
        FIX ME: MATRIX TYPE IS 3D
        FIX ME: MATRIX TYPE IS 3D
        FIX ME: MATRIX TYPE IS 3D
        FIX ME: MATRIX TYPE IS 3D
        FIX ME: MATRIX TYPE IS 3D
        FIX ME: MATRIX TYPE IS 3D
        FIX ME: MATRIX TYPE IS 3D
        FIX ME: MATRIX TYPE IS 3D
        FIX ME: MATRIX TYPE IS 3D
        FIX ME: MATRIX TYPE IS 3D
        FIX ME: MATRIX TYPE IS 3D
        FIX ME: MATRIX TYPE IS 3D
        FIX ME: MATRIX TYPE IS 3D
        FIX ME: MATRIX TYPE IS 3D
        matrix_type = input()
        if matrix_type == 'embedded_score_matrix':
            indel_weight = float(input())
            weights_data = ''
            try:
                while True:
                    weights_data += input() + '\n'
            except EOFError:
                ...
        elif matrix_type == 'file_score_matrix':
            indel_weight = float(input())
            path = input()
            with open(path, mode='r', encoding='utf-8') as f:
                weights_data = f.read()
        else:
            raise ValueError('Bad score matrix type')
        weight_lookup = Table2DWeightLookup.create_from_str(weights_data, indel_weight)
        weight, edges, elems = global_alignment(seqs, weight_lookup)
        print(f'Given the sequences {seqs} and the score matrix...', end="\n\n")
        print(f'```\nINDEL={indel_weight}\n{weights_data}\n````', end="\n\n")
        print(f'... the global alignment is...', end="\n\n")
        for i in range(dims):
            print(f'{"".join("-" if e[i] is None else e[i] for e in elems)}')
        print(f'````', end='\n\n')
        print(f'Weight: {weight}')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()
