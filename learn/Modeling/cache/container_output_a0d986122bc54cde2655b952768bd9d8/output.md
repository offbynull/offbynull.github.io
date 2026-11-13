`{bm-disable-all}`[stats_code/RelativeFrequency.py](stats_code/RelativeFrequency.py) (lines 13 to 16):`{bm-enable-all}`

```python
def relative_frequency(data: list[T]) -> dict[T, int]:
    freqs = frequency(data)
    return {n: f / len(data) for n, f in freqs.items()}
```