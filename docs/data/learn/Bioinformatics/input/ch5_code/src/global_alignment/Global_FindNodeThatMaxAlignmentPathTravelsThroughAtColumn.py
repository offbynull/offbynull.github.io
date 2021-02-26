from typing import TypeVar, List, Tuple

from global_alignment.Global_SweepCombiner import SweepCombiner
from WeightLookup import WeightLookup, Table2DWeightLookup

ELEM = TypeVar('ELEM')


# MARKDOWN
def find_node_that_max_alignment_path_travels_through_at_col(
        v: List[ELEM],
        w: List[ELEM],
        weight_lookup: WeightLookup,
        col: int
) -> Tuple[int, int]:
    col_vals = SweepCombiner(v, w, weight_lookup).get_col(col)
    row, _ = max(enumerate(col_vals), key=lambda x: x[1])
    return col, row


def find_node_that_max_alignment_path_travels_through_at_middle_col(
        v: List[ELEM],
        w: List[ELEM],
        weight_lookup: WeightLookup
) -> Tuple[int, int]:
    v_node_count = len(v) + 1
    middle_col_idx = v_node_count // 2
    return find_node_that_max_alignment_path_travels_through_at_col(v, w, weight_lookup, middle_col_idx)
# MARKDOWN


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        s1 = list(input())
        s2 = list(input())
        col_idx = int(input())
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
        node = find_node_that_max_alignment_path_travels_through_at_col(s1, s2, weight_lookup, col_idx)
        print(f'Given the sequences {"".join(s1)} and {"".join(s2)} and the score matrix...', end="\n\n")
        print(f'```\nINDEL={indel_weight}\n{weights_data}\n````', end="\n\n")
        print(f'... a maximum alignment path is guaranteed to travel through {node}.', end="\n\n")
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()