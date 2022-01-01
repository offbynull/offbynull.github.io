`{bm-disable-all}`[ch8_code/src/metrics/PearsonSimilarity.py](ch8_code/src/metrics/PearsonSimilarity.py) (lines 10 to 17):`{bm-enable-all}`

```python
def pearson_similarity(v: Sequence[float], w: Sequence[float], dims: int):
    v_avg = mean(v)
    w_avg = mean(w)
    vec_avg_diffs_dp = sum((v[i] - v_avg) * (w[i] - w_avg) for i in range(dims))
    dist_to_v_avg = sqrt(sum((v[i] - v_avg) ** 2 for i in range(dims)))
    dist_to_w_avg = sqrt(sum((w[i] - w_avg) ** 2 for i in range(dims)))
    return vec_avg_diffs_dp / (dist_to_v_avg * dist_to_w_avg)
```