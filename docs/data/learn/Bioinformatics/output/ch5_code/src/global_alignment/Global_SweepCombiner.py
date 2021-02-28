from typing import TypeVar, List

from global_alignment.Global_ForwardSweeper import ForwardSweeper
from global_alignment.Global_ReverseSweeper import ReverseSweeper
from scoring.WeightLookup import Table2DWeightLookup, WeightLookup

ELEM = TypeVar('ELEM')

# MARKDOWN
class SweepCombiner:
    def __init__(self, v: List[ELEM], w: List[ELEM], weight_lookup: WeightLookup):
        self.forward_sweeper = ForwardSweeper(v, w, weight_lookup)
        self.reverse_sweeper = ReverseSweeper(v, w, weight_lookup)

    def get_col(self, idx: int):
        fcol = self.forward_sweeper.get_col(idx)
        rcol = self.reverse_sweeper.get_col(idx)
        return [a + b for a, b in zip(fcol, rcol)]
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
        sweep_combiner = SweepCombiner(s1, s2, weight_lookup)
        s1_node_count = len(s1) + 1
        s2_node_count = len(s2) + 1
        cols = sweep_combiner.get_col(col_idx)
        print(f'Given the sequences {"".join(s1)} and {"".join(s2)} and the score matrix...', end="\n\n")
        print(f'```\nINDEL={indel_weight}\n{weights_data}\n````', end="\n\n")
        print(f'... the combined node weights at column {col_idx} are ...', end="\n\n")
        print(f'````')
        for r in range(s2_node_count):
            print('{:6}'.format(cols[r]))
        print(f'````', end="\n\n")
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()
