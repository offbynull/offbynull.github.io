`{bm-disable-all}`[stats_code/StandardDeviation.py](stats_code/StandardDeviation.py) (lines 8 to 13):`{bm-enable-all}`

```python
def population_standard_deviation(data: list[float]) -> float:
    return math.sqrt(population_variance(data))

def sample_standard_deviation(data: list[float]) -> float:
    return math.sqrt(population_variance(data))
```