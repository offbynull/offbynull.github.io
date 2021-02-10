from itertools import product
from typing import List, Any, TypeVar, Tuple

from WeightLookup import WeightLookup, Table2DWeightLookup

ELEM = TypeVar('ELEM')


# MARKDOWN
class ForwardSweeper:
    def __init__(self, v: List[ELEM], w: List[ELEM], weight_lookup: WeightLookup, col_backtrack: int = 2):
        self.v = v
        self.v_node_count = len(v) + 1
        self.w = w
        self.w_node_count = len(w) + 1
        self.weight_lookup = weight_lookup
        self.col_backtrack = col_backtrack
        self.matrix_w_start_idx = 0  # col
        self.matrix = []
        self._reset()

    def _reset(self):
        self.matrix_w_start_idx = 0  # col
        col = [-1.0] * self.v_node_count
        col[0] = 0.0  # source node weight is 0
        for v_idx in range(1, self.v_node_count):
            col[v_idx] = col[v_idx - 1] + self.weight_lookup.lookup(self.v[v_idx - 1], None)
        self.matrix = [col]

    def _step(self):
        next_col = [-1.0] * self.v_node_count
        next_w_idx = self.matrix_w_start_idx + len(self.matrix)
        if len(self.matrix) == self.col_backtrack:
            self.matrix.pop(0)
            self.matrix_w_start_idx += 1
        self.matrix += [next_col]
        self.matrix[-1][0] = self.matrix[-2][0] + self.weight_lookup.lookup(None, self.w[next_w_idx - 1])  # right penalty for first row of new col
        for v_idx in range(1, len(self.v) + 1):
            self.matrix[-1][v_idx] = max(
                self.matrix[-2][v_idx] + self.weight_lookup.lookup(self.v[v_idx - 1], None),                     # right score
                self.matrix[-1][v_idx-1] + self.weight_lookup.lookup(None, self.w[next_w_idx - 1]),              # down score
                self.matrix[-2][v_idx-1] + self.weight_lookup.lookup(self.v[v_idx - 1], self.w[next_w_idx - 1])  # diag score
            )

    def get_col(self, idx: int):
        if idx < self.matrix_w_start_idx:
            self._reset()
        furthest_stored_idx = self.matrix_w_start_idx + len(self.matrix) - 1
        for _ in range(furthest_stored_idx, idx):
            self._step()
        return list(self.matrix[idx - self.matrix_w_start_idx])
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
        forward_sweeper = ForwardSweeper(s1, s2, weight_lookup)
        s1_node_count = len(s1) + 1
        s2_node_count = len(s2) + 1
        cols = []
        for c in range(s2_node_count):
            cols += [forward_sweeper.get_col(c)]
        print(f'Given the sequences {"".join(s1)} and {"".join(s2)} and the score matrix...', end="\n\n")
        print(f'```\nINDEL={indel_weight}\n{weights_data}\n````', end="\n\n")
        print(f'... the node weights are ...', end="\n\n")
        print(f'````')
        for r in range(s1_node_count):
            for c in range(s2_node_count):
                print('{:6}'.format(cols[c][r]), end='')
            print('')
        print(f'````', end="\n\n")
        print(f'The sink node weight (maximum alignment path weight) is {cols[-1][-1]}', end="\n\n")
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()
