`{bm-disable-all}`[stats_code/Mode.py](stats_code/Mode.py) (lines 11 to 15):`{bm-enable-all}`

```python
def mode(data: list[T]) -> tuple[T, int]:
    freqs = frequency(data)
    item, count = max(freqs.items(), key=lambda v: v[1])
    return item, count
```