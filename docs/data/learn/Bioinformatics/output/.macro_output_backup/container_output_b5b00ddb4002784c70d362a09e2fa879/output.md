`{bm-disable-all}`[ch7_code/src/phylogeny/FindNeighbourLimbLengths.py](ch7_code/src/phylogeny/FindNeighbourLimbLengths.py) (lines 12 to 27):`{bm-enable-all}`

```python
def approximate_limb_length_using_neighbour(dm: DistanceMatrix, l: N, l_neighbour: N) -> float:
    leaf_nodes = dm.leaf_ids()
    leaf_nodes.remove(l)
    leaf_nodes.remove(l_neighbour)
    lengths = []
    for k in leaf_nodes:
        length = (dm[l, l_neighbour] + dm[l, k] - dm[l_neighbour, k]) / 2
        lengths.append(length)
    return mean(lengths)


def find_neighbouring_limb_lengths(dm: DistanceMatrix, l1: N, l2: N) -> tuple[float, float]:
    l1_len = approximate_limb_length_using_neighbour(dm, l1, l2)
    l2_len = approximate_limb_length_using_neighbour(dm, l2, l1)
    return l1_len, l2_len
```