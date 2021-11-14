`{bm-disable-all}`[ch7_code/src/sequence_phylogeny/SmallParsimony.py](ch7_code/src/sequence_phylogeny/SmallParsimony.py) (lines 187 to 197):`{bm-enable-all}`

```python
def distance_for_leaf_element_types(
        elem_type_dst: str,
        elem_types: str = 'ACTG'
) -> dict[str, float]:
    dist_set = {}
    for e in elem_types:
        if e == elem_type_dst:
            dist_set[e] = 0.0
        else:
            dist_set[e] = math.inf
    return dist_set
```