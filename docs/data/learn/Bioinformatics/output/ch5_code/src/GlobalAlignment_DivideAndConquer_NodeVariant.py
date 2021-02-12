from typing import TypeVar, List, Tuple

from Global_ForwardSweeper import ForwardSweeper
from Global_ReverseSweeper import ReverseSweeper
from Global_SweepCombiner import SweepCombiner
from WeightLookup import WeightLookup, Table2DWeightLookup

ELEM = TypeVar('ELEM')


def find_middle_node(v: List[ELEM], w: List[ELEM], weight_lookup: WeightLookup) -> Tuple[int, int]:
    v_node_count = len(v) + 1
    w_node_count = len(w) + 1
    middle_col_idx = v_node_count // 2
    middle_col_vals = SweepCombiner(v, w, weight_lookup).get_col(middle_col_idx)
    max_idx_in_middle_col = middle_col_vals.index(max(middle_col_vals))
    return middle_col_idx, max_idx_in_middle_col


def find_max_alignment_path_nodes(
        v: List[ELEM],
        w: List[ELEM],
        weight_lookup: WeightLookup,
        buffer: List[Tuple[int, int]],
        v_offset: int = 0,
        w_offset: int = 0):
    if len(v) == 0 or len(w) == 0:
        return
    c, r = find_middle_node(v, w, weight_lookup)
    find_max_alignment_path_nodes(v[:c-1], w[:r-1], weight_lookup, buffer, v_offset=0, w_offset=0)
    buffer.append((v_offset + c, w_offset + r))
    find_max_alignment_path_nodes(v[c:], w[r:], weight_lookup, buffer, v_offset=v_offset+c, w_offset=v_offset+r)


FIX ME: THIS IS NOT INCLUDING 0,0 AT VERY BEGINING
FIX ME: THIS IS NOT INCLUDING 0,0 AT VERY BEGINING
FIX ME: THIS IS NOT INCLUDING 0,0 AT VERY BEGINING
FIX ME: THIS IS NOT INCLUDING 0,0 AT VERY BEGINING
FIX ME: THIS IS NOT INCLUDING 0,0 AT VERY BEGINING
FIX ME: THIS IS NOT INCLUDING 0,0 AT VERY BEGINING
FIX ME: THIS IS NOT INCLUDING 0,0 AT VERY BEGINING
FIX ME: THIS IS NOT INCLUDING 0,0 AT VERY BEGINING
FIX ME: THIS IS NOT INCLUDING 0,0 AT VERY BEGINING
FIX ME: THIS IS NOT INCLUDING 0,0 AT VERY BEGINING
FIX ME: THIS IS NOT INCLUDING 0,0 AT VERY BEGINING
FIX ME: THIS IS NOT INCLUDING 0,0 AT VERY BEGINING
FIX ME: THIS IS NOT INCLUDING 0,0 AT VERY BEGINING
FIX ME: THIS IS NOT INCLUDING 0,0 AT VERY BEGINING
FIX ME: THIS IS NOT INCLUDING 0,0 AT VERY BEGINING
FIX ME: THIS IS NOT INCLUDING 0,0 AT VERY BEGINING
FIX ME: THIS IS NOT INCLUDING 0,0 AT VERY BEGINING
FIX ME: THIS IS NOT INCLUDING 0,0 AT VERY BEGINING
FIX ME: THIS IS NOT INCLUDING 0,0 AT VERY BEGINING
FIX ME: THIS IS NOT INCLUDING 0,0 AT VERY BEGINING

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
        nodes = []
        find_max_alignment_path_nodes(s1, s2, weight_lookup, nodes)
        print(f'Given the sequences {"".join(s1)} and {"".join(s2)} and the score matrix...', end="\n\n")
        print(f'```\nINDEL={indel_weight}\n{weights_data}\n````', end="\n\n")
        print(f'... a maximum alignment path runs through ...', end="\n\n")
        print(f'{nodes}')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()
