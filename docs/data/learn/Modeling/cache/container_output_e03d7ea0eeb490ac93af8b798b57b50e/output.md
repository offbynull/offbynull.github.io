`{bm-disable-all}`[stats_code/Variance.py](stats_code/Variance.py) (lines 8 to 15):`{bm-enable-all}`

```python
def population_variance(data: list[float]) -> float:
    sq_devs = [deviation(data, i)**2 for i in range(len(data))]
    return mean(sq_devs)

def sample_variance(data: list[float]) -> float:
    sq_devs = [deviation(data, i)**2 for i in range(len(data))]
    return sum(sq_devs) / (len(data) - 1)
```