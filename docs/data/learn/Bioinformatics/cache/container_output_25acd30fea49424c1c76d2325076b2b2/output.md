`{bm-disable-all}`[ch8_code/src/metrics/ManhattanDistance.py](ch8_code/src/metrics/ManhattanDistance.py) (lines 9 to 22):`{bm-enable-all}`

```python
def manhattan_distance(v: Sequence[float], w: Sequence[float], dims: int):
    x = 0.0
    for i in range(dims):
        x += abs(w[i] - v[i])
    return x


# Unsure if this is a good idea, but it I guess it technically meets the definition
# of a similarity metric: the more similar something is, the "greater" the value it
# produces. But, in this case the maximum similarity is 0. Anything less similar is
# negative ("lesser" than 0).
def manhattan_similarity(v: Sequence[float], w: Sequence[float], dims: int):
    return -manhattan_distance(v, w, dims)
```