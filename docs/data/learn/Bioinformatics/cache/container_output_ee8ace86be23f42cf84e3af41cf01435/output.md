`{bm-disable-all}`[ch10_code/src/profile_hmm/AlignmentToProfile.py](ch10_code/src/profile_hmm/AlignmentToProfile.py) (lines 11 to 92):`{bm-enable-all}`

```python
@dataclass
class InsertionColumn(Generic[ELEM]):
    col_from: int
    col_to: int
    values: list[list[ELEM | None]]

    def is_set(self, row: int):
        for v in self.values[row]:
            if v is not None:
                return True
        return False


@dataclass
class NormalColumn(Generic[ELEM]):
    col: int
    values: list[ELEM | None]

    def is_set(self, row: int):
        return self.values[row] is not None


class Profile(Generic[ELEM]):
    def __init__(
            self,
            rows: list[ELEM | None],
            column_removal_threshold: float
    ):
        # This makes sure that the profile starts with an UnstableColumn, ends with an UnstableColumn, and has an
        # UnstableColumn inbetween pairs of StableColumns.
        columns = []
        row_len = len(rows)
        col_len = len(rows[0])
        unstable = None
        for c in range(col_len):
            gap_count = sum(1 for r in range(row_len) if rows[r][c] is None)
            symbol_count = sum(1 for r in range(row_len) if rows[r][c] is not None)
            total_count = gap_count + symbol_count
            perc = gap_count / total_count
            if perc > column_removal_threshold:
                # Create unstable column if it doesn't already exist. Otherwise, increment the "col" coverage on the
                # existing unstable column to indicate that we're adding an extra column to it.
                if unstable is None:
                    unstable = InsertionColumn(c, c, [[] for _ in range(row_len)])
                else:
                    unstable.col_to += 1
                # Add column to the unstable column
                for r in range(row_len):
                    unstable.values[r].append(rows[r][c])
            else:
                # Add pending unstable column, creating an empty one to add if there isn't one pending.
                if unstable is None:
                    unstable = InsertionColumn(-1, -1, [[] for _ in range(row_len)])
                columns.append(unstable)
                # Create and add stable column
                stable = NormalColumn(c, [rows[r][c] for r in range(row_len)])
                columns.append(stable)
                # Reset unstable column
                unstable = None
        # Add last unstable column if required.
        if isinstance(columns[-1], NormalColumn):
            if unstable is None:
                unstable = InsertionColumn(-1, -1, [[] for _ in range(row_len)])
            columns.append(unstable)
        self._columns = columns
        self.col_count = (len(self._columns) - 1) // 2  # num of stable cols
        self.row_count = row_len

    def insertion_before(self, idx: int) -> InsertionColumn:
        idx_of_stable = 1 + (idx * 2)
        idx_of_unstable_before = idx_of_stable - 1
        return self._columns[idx_of_unstable_before]

    def match(self, idx: int) -> NormalColumn:
        idx_of_stable = 1 + (idx * 2)
        return self._columns[idx_of_stable]

    def insertion_after(self, idx: int) -> InsertionColumn:
        idx_of_stable = 1 + (idx * 2)
        idx_of_unstable_after = idx_of_stable + 1
        return self._columns[idx_of_unstable_after]
```