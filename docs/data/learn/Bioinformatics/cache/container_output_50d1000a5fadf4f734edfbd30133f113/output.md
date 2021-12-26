`{bm-disable-all}`[ch8_code/src/metrics/ManhattanDistance.py](ch8_code/src/metrics/ManhattanDistance.py) (lines 9 to 14):`{bm-enable-all}`

```python
def manhattan_distance(v: Sequence[float], w: Sequence[float], dims: int):
    x = 0.0
    for i in range(dims):
        x += abs(w[i] - v[i])
    return x
```