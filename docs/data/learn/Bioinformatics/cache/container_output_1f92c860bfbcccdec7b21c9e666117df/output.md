`{bm-disable-all}`[ch7_code/src/phylogeny/FourPointCondition.py](ch7_code/src/phylogeny/FourPointCondition.py) (lines 43 to 55):`{bm-enable-all}`

```python
def is_additive(dm: DistanceMatrix) -> bool:
    # Recall that an additive distance matrix of size <= 3 is guaranteed to be an additive distance
    # matrix (try it and see -- any distances you use will always end up fitting a tree). Thats why
    # you need at least 4 leaf nodes to test.
    if dm.n < 4:
        return True
    leaves = dm.leaf_ids()
    for quartet in combinations(leaves, r=4):
        passed = four_point_test(dm, *quartet)
        if not passed:
            return False
    return True
```