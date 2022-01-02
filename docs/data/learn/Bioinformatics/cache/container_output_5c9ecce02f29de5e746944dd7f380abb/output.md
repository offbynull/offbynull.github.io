`{bm-disable-all}`[ch8_code/src/metrics/PearsonSimilarity.py](ch8_code/src/metrics/PearsonSimilarity.py) (lines 10 to 28):`{bm-enable-all}`

```python
def pearson_similarity(v: Sequence[float], w: Sequence[float], dims: int):
    v_avg = mean(v)
    w_avg = mean(w)
    vec_avg_diffs_dp = sum((v[i] - v_avg) * (w[i] - w_avg) for i in range(dims))
    dist_to_v_avg = sqrt(sum((v[i] - v_avg) ** 2 for i in range(dims)))
    dist_to_w_avg = sqrt(sum((w[i] - w_avg) ** 2 for i in range(dims)))
    return vec_avg_diffs_dp / (dist_to_v_avg * dist_to_w_avg)


def pearson_distance(v: Sequence[float], w: Sequence[float], dims: int):
    # To turn pearson similarity into a distance metric, subtract 1.0 from it. By
    # subtracting 1.0, you're changing the bounds from [1.0, -1.0] to [0.0, 2.0].
    #
    # Recall that any distance metric must return 0 when the items being compared
    # are the same and increases the more different they get. By subtracting 1.0,
    # you're matching that distance metric requirement: 0.0 when totally similar
    # and 2.0 for totally dissimilar.
    return 1.0 - pearson_similarity(v, w, dims)
```