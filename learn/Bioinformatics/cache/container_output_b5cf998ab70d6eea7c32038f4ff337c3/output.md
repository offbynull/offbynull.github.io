`{bm-disable-all}`[ch7_code/src/phylogeny/CardinalityTest.py](ch7_code/src/phylogeny/CardinalityTest.py) (lines 15 to 19):`{bm-enable-all}`

```python
def cardinality_test(g: Graph[N, ND, E, float]) -> tuple[DistanceMatrix[N], bool]:
    return (
        to_additive_distance_matrix(g),
        is_simple_tree(g)
    )
```