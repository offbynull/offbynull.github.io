`{bm-disable-all}`[ch7_code/src/phylogeny/FindNeighbourLimbLengths.py](ch7_code/src/phylogeny/FindNeighbourLimbLengths.py) (lines 12 to 31):`{bm-enable-all}`

```python
def view_of_limb_length_using_neighbour(dm: DistanceMatrix, l: N, l_neighbour: N, l_from: N) -> float:
    return (dm[l, l_neighbour] + dm[l, l_from] - dm[l_neighbour, l_from]) / 2


def approximate_limb_length_using_neighbour(dm: DistanceMatrix, l: N, l_neighbour: N) -> float:
    leaf_nodes = dm.leaf_ids()
    leaf_nodes.remove(l)
    leaf_nodes.remove(l_neighbour)
    lengths = []
    for l_from in leaf_nodes:
        length = view_of_limb_length_using_neighbour(dm, l, l_neighbour, l_from)
        lengths.append(length)
    return mean(lengths)


def find_neighbouring_limb_lengths(dm: DistanceMatrix, l1: N, l2: N) -> tuple[float, float]:
    l1_len = approximate_limb_length_using_neighbour(dm, l1, l2)
    l2_len = approximate_limb_length_using_neighbour(dm, l2, l1)
    return l1_len, l2_len
```