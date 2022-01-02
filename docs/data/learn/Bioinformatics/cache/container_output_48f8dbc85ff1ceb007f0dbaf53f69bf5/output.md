`{bm-disable-all}`[ch8_code/src/metrics/CosineSimilarity.py](ch8_code/src/metrics/CosineSimilarity.py) (lines 9 to 25):`{bm-enable-all}`

```python
def cosine_similarity(v: Sequence[float], w: Sequence[float], dims: int):
    vec_dp = sum(v[i] * w[i] for i in range(dims))
    v_mag = sqrt(sum(v[i] ** 2 for i in range(dims)))
    w_mag = sqrt(sum(w[i] ** 2 for i in range(dims)))
    return vec_dp / (v_mag * w_mag)


def cosine_distance(v: Sequence[float], w: Sequence[float], dims: int):
    # To turn cosine similarity into a distance metric, subtract 1.0 from it. By
    # subtracting 1.0, you're changing the bounds from [1.0, -1.0] to [0.0, 2.0].
    #
    # Recall that any distance metric must return 0 when the items being compared
    # are the same and increases the more different they get. By subtracting 1.0,
    # you're matching that distance metric requirement: 0.0 when totally similar
    # and 2.0 for totally dissimilar.
    return 1.0 - cosine_similarity(v, w, dims)
```