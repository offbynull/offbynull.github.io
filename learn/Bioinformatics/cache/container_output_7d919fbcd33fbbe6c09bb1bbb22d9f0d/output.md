`{bm-disable-all}`[ch5_code/src/global_alignment/Global_ForwardSweeper.py](ch5_code/src/global_alignment/Global_ForwardSweeper.py) (lines 9 to 51):`{bm-enable-all}`

```python
class ForwardSweeper:
    def __init__(self, v: List[ELEM], w: List[ELEM], weight_lookup: WeightLookup, col_backtrack: int = 2):
        self.v = v
        self.v_node_count = len(v) + 1
        self.w = w
        self.w_node_count = len(w) + 1
        self.weight_lookup = weight_lookup
        self.col_backtrack = col_backtrack
        self.matrix_v_start_idx = 0  # col
        self.matrix = []
        self._reset()

    def _reset(self):
        self.matrix_v_start_idx = 0  # col
        col = [-1.0] * self.w_node_count
        col[0] = 0.0  # source node weight is 0
        for w_idx in range(1, self.w_node_count):
            col[w_idx] = col[w_idx - 1] + self.weight_lookup.lookup(None, self.w[w_idx - 1])
        self.matrix = [col]

    def _step(self):
        next_col = [-1.0] * self.w_node_count
        next_v_idx = self.matrix_v_start_idx + len(self.matrix)
        if len(self.matrix) == self.col_backtrack:
            self.matrix.pop(0)
            self.matrix_v_start_idx += 1
        self.matrix += [next_col]
        self.matrix[-1][0] = self.matrix[-2][0] + self.weight_lookup.lookup(self.v[next_v_idx - 1], None)  # right penalty for first row of new col
        for w_idx in range(1, len(self.w) + 1):
            self.matrix[-1][w_idx] = max(
                self.matrix[-2][w_idx] + self.weight_lookup.lookup(None, self.w[w_idx - 1]),                     # right score
                self.matrix[-1][w_idx-1] + self.weight_lookup.lookup(self.v[next_v_idx - 1], None),              # down score
                self.matrix[-2][w_idx-1] + self.weight_lookup.lookup(self.v[next_v_idx - 1], self.w[w_idx - 1])  # diag score
            )

    def get_col(self, idx: int):
        if idx < self.matrix_v_start_idx:
            self._reset()
        furthest_stored_idx = self.matrix_v_start_idx + len(self.matrix) - 1
        for _ in range(furthest_stored_idx, idx):
            self._step()
        return list(self.matrix[idx - self.matrix_v_start_idx])
```