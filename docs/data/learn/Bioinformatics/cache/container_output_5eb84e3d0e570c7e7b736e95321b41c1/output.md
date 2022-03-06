```python
# Distorted avg -- like avg, but reduces the influence of outliers. The larger e is, the
# less influence the outlier will have.
def distorted_avg(values: list[float], e: float) -> float:
    count = len(values)
    return (sum(v ** (1 / e) for v in values) / count) ** e
```