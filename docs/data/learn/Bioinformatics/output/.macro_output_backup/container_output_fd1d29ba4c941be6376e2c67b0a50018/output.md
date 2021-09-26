`{bm-disable-all}`[ch7_code/src/phylogeny/BaldDistanceMatrix.py](ch7_code/src/phylogeny/BaldDistanceMatrix.py) (lines 14 to 20):`{bm-enable-all}`

```python
def bald(dm: DistanceMatrix, l: N) -> None:
    l_len = limb_length(dm, l)
    for n in dm.leaf_ids_it():
        if n == l:
            continue
        dm[l, n] -= l_len
```