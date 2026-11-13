`{bm-disable-all}`[ch8_code/src/metrics/EuclideanDistance.py](ch8_code/src/metrics/EuclideanDistance.py) (lines 9 to 22):`{bm-enable-all}`

```python
def euclidean_distance(v: Sequence[float], w: Sequence[float], dims: int):
    x = 0.0
    for i in range(dims):
        x += (w[i] - v[i]) ** 2
    return sqrt(x)


# Unsure if this is a good idea, but it I guess it technically meets the definition
# of a similarity metric: the more similar something is, the "greater" the value it
# produces. But, in this case the maximum similarity is 0. Anything less similar is
# negative ("lesser" than 0).
def euclidean_similarity(v: Sequence[float], w: Sequence[float], dims: int):
    return -euclidean_distance(v, w, dims)
```