`{bm-disable-all}`[stats_code/Quartile.py](stats_code/Quartile.py) (lines 18 to 21):`{bm-enable-all}`

```python
def iqr(data: list[float]) -> float:
    q1, _, q3 = quartiles_at(data)
    return q3 - q1
```