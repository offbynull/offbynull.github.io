from itertools import product
from typing import List, Any, TypeVar, Tuple

from WeightLookup import WeightLookup, Table2DWeightLookup

ELEM = TypeVar('ELEM')


# MARKDOWN
def backtrack(
        node_matrix: List[List[Any]]
) -> Tuple[float, List[Tuple[ELEM, ELEM]]]:
    v_node_idx = len(node_matrix) - 1
    w_node_idx = len(node_matrix[0]) - 1
    final_weight = node_matrix[v_node_idx][w_node_idx][0]
    alignment = []
    while v_node_idx >= 0 and w_node_idx > 0:
        _, elems, backtrack_ptr = node_matrix[v_node_idx][w_node_idx]
        if backtrack_ptr == '↓':
            v_node_idx -= 1
        elif backtrack_ptr == '→':
            w_node_idx -= 1
        elif backtrack_ptr == '↘':
            v_node_idx -= 1
            w_node_idx -= 1
        alignment.append(elems)
    return final_weight, alignment[::-1]


def global_alignment(
        v: List[ELEM],
        w: List[ELEM],
        weight_lookup: WeightLookup
) -> Tuple[float, List[Tuple[ELEM, ELEM]]]:
    v_node_count = len(v) + 1
    w_node_count = len(w) + 1
    node_matrix = []
    for v_node_idx in range(v_node_count):
        row = []
        for w_node_idx in range(w_node_count):
            row.append([-1.0, (None, None), '?'])
        node_matrix.append(row)
    node_matrix[0][0][0] = 0.0           # source node weight
    node_matrix[0][0][1] = (None, None)  # source node elements (elements don't matter for source node)
    node_matrix[0][0][2] = '↘'           # source node backtracking edge (direction doesn't matter for source node)
    for v_node_idx in range(1, v_node_count):
        v_elem = v[v_node_idx - 1]
        elems = v_elem, None
        node_matrix[v_node_idx][0][0] = weight_lookup.lookup(*elems)
        node_matrix[v_node_idx][0][1] = elems
        node_matrix[v_node_idx][0][2] = '↓'
    for w_node_idx in range(1, w_node_count):
        w_elem = w[w_node_idx - 1]
        elems = None, w_elem
        node_matrix[0][w_node_idx][0] = weight_lookup.lookup(*elems)
        node_matrix[0][w_node_idx][1] = elems
        node_matrix[0][w_node_idx][2] = '→'
    for v_node_idx, w_node_idx in product(range(1, v_node_count), range(1, w_node_count)):
        v_elem = v[v_node_idx - 1]
        w_elem = w[w_node_idx - 1]
        node_matrix[v_node_idx][w_node_idx] = max(
            [node_matrix[v_node_idx - 1][w_node_idx][0] + weight_lookup.lookup(v_elem, None), (v_elem, None), '↓'],
            [node_matrix[v_node_idx][w_node_idx - 1][0] + weight_lookup.lookup(None, w_elem), (None, w_elem), '→'],
            [node_matrix[v_node_idx - 1][w_node_idx - 1][0] + weight_lookup.lookup(v_elem, w_elem), (v_elem, w_elem), '↘'],
            key=lambda x: x[0]
        )
    return backtrack(node_matrix)
# MARKDOWN


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        s1 = list(input())
        s2 = list(input())
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
        weight, elems = global_alignment(s1, s2, weight_lookup)
        print(f'Given the sequences {"".join(s1)} and {"".join(s2)} and the score matrix...', end="\n\n")
        print(f'```\nINDEL={indel_weight}\n{weights_data}\n````', end="\n\n")
        print(f'... the global alignment is...', end="\n\n")
        print(f'````')
        print(f'{"".join("-" if e[0] is None else e[0] for e in elems)}')
        print(f'{"".join("-" if e[1] is None else e[1] for e in elems)}')
        print(f'````', end='\n\n')
        print(f'Weight: {weight}')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()
