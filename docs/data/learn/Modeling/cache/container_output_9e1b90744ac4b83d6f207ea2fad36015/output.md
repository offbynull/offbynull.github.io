`{bm-disable-all}`[stats_code/Quartile.py](stats_code/Quartile.py) (lines 10 to 14):`{bm-enable-all}`

```python
def quartiles_at(data: list[T]) -> tuple[float, float, float]:
    return percentile_at(data, 0.25), \
        percentile_at(data, 0.5), \
        percentile_at(data, 0.75)
```