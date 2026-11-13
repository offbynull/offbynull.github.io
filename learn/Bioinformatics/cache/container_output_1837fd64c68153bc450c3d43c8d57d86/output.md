`{bm-disable-all}`[ch2_code/src/ScoreMotif.py](ch2_code/src/ScoreMotif.py) (lines 17 to 39):`{bm-enable-all}`

```python
def score_motif(motif_matrix: List[str]) -> int:
    rows = len(motif_matrix)
    cols = len(motif_matrix[0])

    # count up each column
    counter_per_col = []
    for c in range(0, cols):
        counter = Counter()
        for r in range(0, rows):
            counter[motif_matrix[r][c]] += 1
        counter_per_col.append(counter)

    # sum counts for each column AFTER removing the top-most count -- that is, consider the top-most count as the
    # most popular char, so you're summing the counts of all the UNPOPULAR chars
    unpopular_sums = []
    for counter in counter_per_col:
        most_popular_item = counter.most_common(1)[0][0]
        del counter[most_popular_item]
        unpopular_sum = sum(counter.values())
        unpopular_sums.append(unpopular_sum)

    return sum(unpopular_sums)
```