`{bm-disable-all}`[stats_code/CumulativeFrequency.py](stats_code/CumulativeFrequency.py) (lines 14 to 32):`{bm-enable-all}`

```python
def cumulative_frequency(data: list[T]) -> dict[T, int]:
    freqs = frequency(data)
    cum_freqs = {}
    last_val = 0
    for item in sorted(freqs):
        last_val += freqs[item]
        cum_freqs[item] = last_val
    return cum_freqs


def cumulative_relative_frequency(data: list[T]) -> dict[T, int]:
    freqs = relative_frequency(data)
    cum_freqs = {}
    last_val = 0
    for item in sorted(freqs):
        last_val += freqs[item]
        cum_freqs[item] = last_val
    return cum_freqs
```