from typing import Dict, Tuple, List

from helpers.Utils import range_inclusive

# DON'T USE THIS -- THERE ARE CLEAN IMPLEMENTATIONS OF THE DIFFERENT ALGORITHMS IN THE SUBDIRECTORIES.
# DON'T USE THIS -- THERE ARE CLEAN IMPLEMENTATIONS OF THE DIFFERENT ALGORITHMS IN THE SUBDIRECTORIES.
# DON'T USE THIS -- THERE ARE CLEAN IMPLEMENTATIONS OF THE DIFFERENT ALGORITHMS IN THE SUBDIRECTORIES.

#
# Load scoring matrix
#
indel_penalty = -5  # specified in problem statement
mismatch_penalties: Dict[Tuple[str, str], int] = {}
with open('BLOSUM62.txt', mode='r', encoding='utf-8') as f:
    data = f.read()
lines = data.strip().split('\n')
aa_row = lines[0].strip().split()
for line in lines[1:]:
    vals = line.strip().split()
    aa2 = vals[0]
    weight = vals[1:]
    for aa1, weight in zip(aa_row, weight):
        mismatch_penalties[(aa1, aa2)] = int(weight)


#
# Load sequences
#
with open('/home/user/Downloads/dataset_240308_14.txt', mode='r', encoding='utf-8') as f:
    data = f.read()

lines = data.strip().split('\n')
s1 = list(lines[0].strip())
s2 = list(lines[1].strip())


class ForwardSweeper:
    def __init__(self, v: List[str], w: List[str], col_backtrack: int = 2):
        self.v = v
        self.w = w
        self.col_backtrack = col_backtrack
        self.matrix_w_start_idx = 0  # col
        self.matrix = []
        self._reset()

    def _reset(self):
        self.matrix_w_start_idx = 0  # col
        col = [-1] * (len(self.v) + 1)
        for v_idx in range(len(self.v) + 1):
            col[v_idx] = indel_penalty * v_idx
        self.matrix = [col]

    def _step(self):
        next_col = [-1] * (len(self.v) + 1)
        next_w_idx = self.matrix_w_start_idx + len(self.matrix)
        if len(self.matrix) == self.col_backtrack:
            self.matrix.pop(0)
            self.matrix_w_start_idx += 1
        self.matrix += [next_col]
        self.matrix[-1][0] = self.matrix[-2][0] + indel_penalty  # right penalty for first row of new col
        for v_idx in range(1, len(self.v) + 1):
            self.matrix[-1][v_idx] = max(
                self.matrix[-2][v_idx] + indel_penalty,  # right penalty
                self.matrix[-1][v_idx-1] + indel_penalty,  # down penalty
                self.matrix[-2][v_idx-1] + mismatch_penalties[(self.v[v_idx - 1], self.w[next_w_idx - 1])]
            )

    def get_col(self, idx: int):
        if idx < self.matrix_w_start_idx:
            self._reset()
        furthest_stored_idx = self.matrix_w_start_idx + len(self.matrix) - 1
        for _ in range(furthest_stored_idx, idx):
            self._step()
        return list(self.matrix[idx - self.matrix_w_start_idx])


# SWEEP in reverse from bottom right to top left -- pretend like the direction of each edge is flipped.
class ReverseSweeper:
    def __init__(self, v: List[str], w: List[str], col_fronttrack: int = 2):
        self.v = v
        self.w = w
        self.col_fronttrack = col_fronttrack
        self.matrix_w_end_idx = len(self.w)  # col
        self.matrix = []
        self._reset()

    def _reset(self):
        self.matrix_w_end_idx = len(self.w)  # col
        col = [-1] * (len(self.v) + 1)
        for v_idx in range(len(col)):
            col[len(col) - v_idx - 1] = indel_penalty * v_idx
        self.matrix = [col]

    def _step(self):
        prev_col = [-9999] * (len(self.v) + 1)
        prev_w_idx = self.matrix_w_end_idx - len(self.matrix)
        if len(self.matrix) == self.col_fronttrack:
            self.matrix.pop()
            self.matrix_w_end_idx -= 1
        self.matrix.insert(0, prev_col)
        self.matrix[0][len(self.v)] = self.matrix[1][len(self.v)] + indel_penalty  # left penalty for last row of new col
        for v_idx in range_inclusive(len(self.v) - 1, 0, -1):
            self.matrix[0][v_idx] = max(
                self.matrix[1][v_idx] + indel_penalty,  # left penalty
                self.matrix[0][v_idx+1] + indel_penalty,  # up penalty
                self.matrix[1][v_idx+1] + mismatch_penalties[(self.v[v_idx], self.w[prev_w_idx])]
            )

    def get_col(self, idx: int):
        if idx > self.matrix_w_end_idx:
            self._reset()
        closest_stored_idx = self.matrix_w_end_idx - len(self.matrix)
        for _ in range_inclusive(closest_stored_idx, idx, -1):
            self._step()
        start_idx = self.matrix_w_end_idx - len(self.matrix) + 1
        offset_idx = idx - start_idx
        return list(self.matrix[offset_idx])


# Does the same thing as ReverseSweeper, but uses ForwardSwepper and instead reverses the strings
class ReverseSweeperWrapped:
    def __init__(self, v: List[str], w: List[str], col_fronttrack: int = 2):
        self.backing = ForwardSweeper(v[::-1], w[::-1], col_fronttrack)

    def get_col(self, idx: int):
        return self.backing.get_col(len(self.backing.w) - idx)[::-1]


class SweepCombiner:
    def __init__(self, v: List[str], w: List[str]):
        self.forward_sweeper = ForwardSweeper(v, w)
        self.reverse_sweeper = ReverseSweeper(v, w)

    def get_col(self, idx: int):
        fcol = self.forward_sweeper.get_col(idx)
        rcol = self.reverse_sweeper.get_col(idx)
        return [a + b for a, b in zip(fcol, rcol)]



def lcs(v: List[str], w: List[str]):
    lcs_matrix = [[-1] * (len(v) + 1) for i in range(len(w) + 1)]
    for i in range(len(v) + 1):
        lcs_matrix[0][i] = indel_penalty * i
    for j in range(len(w) + 1):
        lcs_matrix[j][0] = indel_penalty * j
    for j in range(1, len(w) + 1):
        for i in range(1, len(v) + 1):
            match = mismatch_penalties[(v[i - 1], w[j - 1])]
            lcs_matrix[j][i] = max(
                lcs_matrix[j - 1][i] + indel_penalty,
                lcs_matrix[j][i - 1] + indel_penalty,
                lcs_matrix[j - 1][i - 1] + match
            )
    return lcs_matrix


def find_middle_edge(s1: List[str], s2: List[str]):
    sc = SweepCombiner(s1, s2)
    middle_col = len(s2) // 2
    middle_col_res = sc.get_col(middle_col)
    next_col_res = sc.get_col(middle_col + 1)
    middle_col_max_row, _ = max(enumerate(middle_col_res), key=lambda x: x[1])
    neighbours = []
    # len(s2) + 1 = len(node columns produced for s2),  len(s1) + 1 = len(node rows produced for s1)
    if middle_col + 1 < len(s2) + 1:
        neighbours += [(next_col_res[middle_col_max_row], (middle_col_max_row, middle_col + 1))]
    if middle_col_max_row + 1 < len(s1) + 1 and middle_col < len(s2) + 1:
        neighbours += [(next_col_res[middle_col_max_row + 1], (middle_col_max_row + 1, middle_col + 1))]
    if middle_col_max_row + 1 < len(s1) + 1:
        neighbours += [(middle_col_res[middle_col_max_row + 1], (middle_col_max_row + 1, middle_col))]
    _, (next_row, next_col) = max(neighbours, key=lambda x: x[0])
    return (middle_col_max_row, middle_col), (next_row, next_col)


def linear_space_alignment(v, w, top, bottom, left, right, output):
    if left == right:
        for i in range(top, bottom):
            output += ['↓']
        return
    if top == bottom:
        for i in range(left, right):
            output += ['→']
        return

    (node1_row, node1_col), (node2_row, node2_col) = find_middle_edge(s1[top:bottom], s2[left:right])
    middle_col = left + node1_col
    middle_row = top + node1_row
    linear_space_alignment(v, w, top, middle_row, left, middle_col, output)
    if node1_row + 1 == node2_row and node1_col + 1 == node2_col:
        edge_dir = '↘'
    elif node1_row == node2_row and node1_col + 1 == node2_col:
        edge_dir = '→'
    elif node1_row + 1 == node2_row and node1_col == node2_col:
        edge_dir = '↓'
    else:
        raise ValueError()
    if edge_dir == '→' or edge_dir == '↘':
        middle_col = middle_col + 1
    if edge_dir == '↓' or edge_dir == '↘':
        middle_row = middle_row + 1
    output += [edge_dir]
    linear_space_alignment(v, w, middle_row, bottom, middle_col, right, output)


output = []
linear_space_alignment(s1, s2, 0, len(s1), 0, len(s2), output)

# print(f'{output}')

s1_align = ''
s2_align = ''
weight = 0
for edge_dir in output:
    if edge_dir == '↓':
        s1_align += s1.pop(0)
        s2_align += '-'
        weight += indel_penalty
    elif edge_dir == '↘':
        s1_align += s1.pop(0)
        s2_align += s2.pop(0)
        weight += mismatch_penalties[(s1_align[-1], s2_align[-1])]
    elif edge_dir == '→':
        s1_align += '-'
        s2_align += s2.pop(0)
        weight += indel_penalty
    else:
        raise ValueError()

print(weight)
print(s1_align)
print(s2_align)
