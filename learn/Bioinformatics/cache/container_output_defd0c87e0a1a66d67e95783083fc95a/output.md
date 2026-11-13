`{bm-disable-all}`[ch2_code/src/MotifMatrixProfile.py](ch2_code/src/MotifMatrixProfile.py) (lines 8 to 22):`{bm-enable-all}`

```python
def motif_matrix_profile(motif_matrix_counts: Dict[str, List[int]]) -> Dict[str, List[float]]:
    ret = {}
    for elem, counts in motif_matrix_counts.items():
        ret[elem] = [0.0] * len(counts)

    cols = len(counts)  # all elems should have the same len, so just grab the last one that was walked over
    for i in range(cols):
        total = 0
        for elem in motif_matrix_counts.keys():
            total += motif_matrix_counts[elem][i]
        for elem in motif_matrix_counts.keys():
            ret[elem][i] = motif_matrix_counts[elem][i] / total

    return ret
```