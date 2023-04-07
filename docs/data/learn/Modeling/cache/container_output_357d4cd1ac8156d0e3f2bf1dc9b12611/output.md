`{bm-disable-all}`[stats_code/Frequency.py](stats_code/Frequency.py) (lines 11 to 17):`{bm-enable-all}`

```python
def frequency(data: list[T]) -> dict[T, int]:
    ret = {}
    for v in data:
        v_freq = ret.get(v, 0) + 1
        ret[v] = v_freq
    return ret
```