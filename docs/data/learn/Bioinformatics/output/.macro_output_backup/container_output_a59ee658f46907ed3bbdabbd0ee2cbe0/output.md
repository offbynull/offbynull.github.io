`{bm-disable-all}`[ch7_code/src/phylogeny/AdditiveDistanceMatrixTest_FourPointCondition.py](ch7_code/src/phylogeny/AdditiveDistanceMatrixTest_FourPointCondition.py) (lines 12 to 35):`{bm-enable-all}`

```python
def four_point_test(dm: DistanceMatrix, l0: N, l1: N, l2: N, l3: N) -> bool:
    # Pairs of leaf node pairs
    pair_combos = (
        ((l0, l1), (l2, l3)),
        ((l0, l2), (l1, l3)),
        ((l0, l3), (l1, l2))
    )
    # Different orders to test pair_combos to see if they match conditions
    test_orders = (
        (0, 1, 2),
        (0, 2, 1),
        (1, 2, 0)
    )
    # Find at least one order of pair combos that passes the test
    for p1_idx, p2_idx, p3_idx in test_orders:
        p1_1, p1_2 = pair_combos[p1_idx]
        p2_1, p2_2 = pair_combos[p2_idx]
        p3_1, p3_2 = pair_combos[p3_idx]
        s1 = dm[p1_1] + dm[p1_2]
        s2 = dm[p2_1] + dm[p2_2]
        s3 = dm[p3_1] + dm[p3_2]
        if s1 <= s2 == s3:
            return True
    return False
```