`{bm-disable-all}`[ch8_code/src/metrics/CosineSimilarity.py](ch8_code/src/metrics/CosineSimilarity.py) (lines 9 to 14):`{bm-enable-all}`

```python
def cosine_similarity(v: Sequence[float], w: Sequence[float], dims: int):
    vec_dp = sum(v[i] * w[i] for i in range(dims))
    v_mag = sqrt(sum(v[i] ** 2 for i in range(dims)))
    w_mag = sqrt(sum(w[i] ** 2 for i in range(dims)))
    return vec_dp / (v_mag * w_mag)
```