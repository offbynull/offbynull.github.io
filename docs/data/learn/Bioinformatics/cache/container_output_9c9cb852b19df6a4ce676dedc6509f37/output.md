`{bm-disable-all}`[ch8_code/src/metrics/EuclideanDistance.py](ch8_code/src/metrics/EuclideanDistance.py) (lines 9 to 14):`{bm-enable-all}`

```python
def euclidean_distance(v: Sequence[float], w: Sequence[float], dims: int):
    x = 0.0
    for i in range(dims):
        x += (w[i] - v[i]) ** 2
    return sqrt(x)
```