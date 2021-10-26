`{bm-disable-all}`[ch7_code/src/phylogeny/SubtreeDetect.py](ch7_code/src/phylogeny/SubtreeDetect.py) (lines 14 to 23):`{bm-enable-all}`

```python
def is_same_subtree(dm: DistanceMatrix, l: N, a: N, b: N) -> bool:
    l_weight = find_limb_length(dm, l)
    test_res = (dm[l, a] + dm[l, b] - dm[a, b]) / 2
    if test_res == l_weight:
        return False
    elif test_res > l_weight:
        return True
    else:
        raise ValueError('???')  # not additive distance matrix?
```