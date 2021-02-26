from typing import TypeVar, List, Tuple

from global_alignment import GlobalAlignment_Matrix
from global_alignment.Global_FindNodeThatMaxAlignmentPathTravelsThroughAtColumn import \
    find_node_that_max_alignment_path_travels_through_at_middle_col
from WeightLookup import WeightLookup, Table2DWeightLookup

ELEM = TypeVar('ELEM')

# MARKDOWN
def find_max_alignment_path_nodes(
        v: List[ELEM],
        w: List[ELEM],
        weight_lookup: WeightLookup,
        buffer: List[Tuple[int, int]],
        v_offset: int = 0,
        w_offset: int = 0) -> None:
    if len(v) == 0 or len(w) == 0:
        return
    c, r = find_node_that_max_alignment_path_travels_through_at_middle_col(v, w, weight_lookup)
    find_max_alignment_path_nodes(v[:c-1], w[:r-1], weight_lookup, buffer, v_offset=0, w_offset=0)
    buffer.append((v_offset + c, w_offset + r))
    find_max_alignment_path_nodes(v[c:], w[r:], weight_lookup, buffer, v_offset=v_offset+c, w_offset=v_offset+r)


def global_alignment(
        v: List[ELEM],
        w: List[ELEM],
        weight_lookup: WeightLookup
) -> Tuple[float, List[Tuple[ELEM, ELEM]]]:
    nodes = [(0, 0)]
    find_max_alignment_path_nodes(v, w, weight_lookup, nodes)
    weight = 0.0
    alignment = []
    for (v_idx1, w_idx1), (v_idx2, w_idx2) in zip(nodes, nodes[1:]):
        sub_weight, sub_alignment = GlobalAlignment_Matrix.global_alignment(v[v_idx1:v_idx2], w[w_idx1:w_idx2], weight_lookup)
        weight += sub_weight
        alignment += sub_alignment
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
        weight_lookup = Table2DWeightLookup.create_from_2d_matrix_str(weights_data, indel_weight)
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
