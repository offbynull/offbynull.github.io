`{bm-disable-all}`[ch2_code/src/MotifMatrixCount.py](ch2_code/src/MotifMatrixCount.py) (lines 7 to 21):`{bm-enable-all}`

```python
def motif_matrix_count(motif_matrix: List[str], elements='ACGT') -> Dict[str, List[int]]:
    rows = len(motif_matrix)
    cols = len(motif_matrix[0])

    ret = {}
    for ch in elements:
        ret[ch] = [0] * cols
    
    for c in range(0, cols):
        for r in range(0, rows):
            item = motif_matrix[r][c]
            ret[item][c] += 1
            
    return ret
```