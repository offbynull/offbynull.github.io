from typing import TypeVar, List, Tuple

import GlobalAlignment_Matrix
from Global_FindEdgeThatMaxAlignmentPathTravelsThroughAtColumn import \
    find_edge_that_max_alignment_path_travels_through_at_middle_col
from Global_FindNodeThatMaxAlignmentPathTravelsThroughAtColumn import \
    find_node_that_max_alignment_path_travels_through_at_middle_col
from WeightLookup import WeightLookup, Table2DWeightLookup

ELEM = TypeVar('ELEM')

# MARKDOWN
def find_max_alignment_path_edges(
        v: List[ELEM],
        w: List[ELEM],
        weight_lookup: WeightLookup,
        top: int,
        bottom: int,
        left: int,
        right: int,
        output: List[str]):
    if left == right:
        for i in range(top, bottom):
            output += ['↓']
        return
    if top == bottom:
        for i in range(left, right):
            output += ['→']
        return

    (col1, row1), (col2, row2) = find_edge_that_max_alignment_path_travels_through_at_middle_col(v[left:right], w[top:bottom], weight_lookup)
    middle_col = left + col1
    middle_row = top + row1
    find_max_alignment_path_edges(v, w, weight_lookup, top, middle_row, left, middle_col, output)
    if row1 + 1 == row2 and col1 + 1 == col2:
        edge_dir = '↘'
    elif row1 == row2 and col1 + 1 == col2:
        edge_dir = '→'
    elif row1 + 1 == row2 and col1 == col2:
        edge_dir = '↓'
    else:
        raise ValueError()
    if edge_dir == '→' or edge_dir == '↘':
        middle_col += 1
    if edge_dir == '↓' or edge_dir == '↘':
        middle_row += 1
    output += [edge_dir]
    find_max_alignment_path_edges(v, w, weight_lookup, middle_row, bottom, middle_col, right, output)


def global_alignment(
        v: List[ELEM],
        w: List[ELEM],
        weight_lookup: WeightLookup
) -> Tuple[float, List[Tuple[ELEM, ELEM]]]:
    edges = []
    find_max_alignment_path_edges(v, w, weight_lookup, 0, len(w), 0, len(v), edges)
    weight = 0.0
    alignment = []
    v_idx = 0
    w_idx = 0
    for edge in edges:
        if edge == '→':
            v_elem = v[v_idx]
            w_elem = None
            alignment.append((v_elem, w_elem))
            weight += weight_lookup.lookup(v_elem, w_elem)
            v_idx += 1
        elif edge == '↓':
            v_elem = None
            w_elem = w[w_idx]
            alignment.append((v_elem, w_elem))
            weight += weight_lookup.lookup(v_elem, w_elem)
            w_idx += 1
        elif edge == '↘':
            v_elem = v[v_idx]
            w_elem = w[w_idx]
            alignment.append((v_elem, w_elem))
            weight += weight_lookup.lookup(v_elem, w_elem)
            v_idx += 1
            w_idx += 1
    return weight, alignment
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
