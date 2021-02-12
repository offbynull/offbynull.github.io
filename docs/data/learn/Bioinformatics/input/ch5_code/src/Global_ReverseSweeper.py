from itertools import product
from typing import List, Any, TypeVar, Tuple

from Global_ForwardSweeper import ForwardSweeper
from WeightLookup import WeightLookup, Table2DWeightLookup

ELEM = TypeVar('ELEM')


# MARKDOWN
class ReverseSweeper:
    def __init__(self, v: List[ELEM], w: List[ELEM], weight_lookup: WeightLookup, col_fronttrack: int = 2):
        self.v = v
        self.v_node_count = len(v) + 1
        self.w = w
        self.w_node_count = len(w) + 1
        self.weight_lookup = weight_lookup
        self.col_fronttrack = col_fronttrack
        self.matrix_v_end_idx = self.v_node_count - 1  # col
        self.matrix = []
        self._reset()

    def _reset(self):
        self.matrix_v_end_idx = self.v_node_count - 1  # col
        col = [-1.0] * self.w_node_count
        col[-1] = 0.0  # source node weight is 0
        for w_idx in range(self.w_node_count - 2, -1, -1):  # from 2nd last to 0
            col[w_idx] = col[w_idx + 1] + self.weight_lookup.lookup(None, self.w[w_idx - 1])
        self.matrix = [col]

    def _step(self):
        prev_col = [-9999.0] * self.w_node_count
        prev_v_idx = self.matrix_v_end_idx - len(self.matrix)
        if len(self.matrix) == self.col_fronttrack:
            self.matrix.pop()
            self.matrix_v_end_idx -= 1
        self.matrix.insert(0, prev_col)
        self.matrix[0][-1] = self.matrix[1][-1] + self.weight_lookup.lookup(self.v[prev_v_idx], None)  # left penalty for first row of new col
        for w_idx in range(self.w_node_count - 2, -1, -1):  # from 2nd last to 0
            self.matrix[0][w_idx] = max(
                self.matrix[1][w_idx] + self.weight_lookup.lookup(None, self.w[w_idx]),                 # left score
                self.matrix[0][w_idx+1] + self.weight_lookup.lookup(self.v[prev_v_idx], None),          # up score
                self.matrix[1][w_idx+1] + self.weight_lookup.lookup(self.v[prev_v_idx], self.w[w_idx])  # diag score
            )

    def get_col(self, idx: int):
        if idx > self.matrix_v_end_idx:
            self._reset()
        closest_stored_idx = self.matrix_v_end_idx - len(self.matrix)
        for _ in range(closest_stored_idx, idx - 1, -1):  # from closest_stored_idx to idx
            self._step()
        start_idx = self.matrix_v_end_idx - len(self.matrix) + 1
        offset_idx = idx - start_idx
        return list(self.matrix[offset_idx])
# MARKDOWN


# Does the same thing as ReverseSweeper, but uses ForwardSwepper and instead reverses the strings
class ReverseSweeperWrapped:
    def __init__(self, v: List[str], w: List[str], weight_lookup: WeightLookup, col_fronttrack: int = 2):
        self.backing = ForwardSweeper(v[::-1], w[::-1], weight_lookup, col_fronttrack)

    def get_col(self, idx: int):
        return self.backing.get_col(len(self.backing.w) - idx)[::-1]


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
        forward_sweeper = ReverseSweeper(s1, s2, weight_lookup)
        s1_node_count = len(s1) + 1
        s2_node_count = len(s2) + 1
        cols = []
        for c in range(s1_node_count):
            cols += [forward_sweeper.get_col(c)]
        print(f'Given the sequences {"".join(s1)} and {"".join(s2)} and the score matrix...', end="\n\n")
        print(f'```\nINDEL={indel_weight}\n{weights_data}\n````', end="\n\n")
        print(f'... the node weights are ...', end="\n\n")
        print(f'````')
        for r in range(s2_node_count):
            for c in range(s1_node_count):
                print('{:6}'.format(cols[c][r]), end='')
            print('')
        print(f'````', end="\n\n")
        print(f'The sink node weight (maximum alignment path weight) is {cols[-1][-1]}', end="\n\n")
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()
