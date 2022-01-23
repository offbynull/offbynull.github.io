```python
def center_of_gravity(
        points: list[tuple[float]],
        dims: int
) -> tuple[float]:
    center = []
    for i in range(dims):
        val = mean(pt[i] for pt in points)
        center.append(val)
    return tuple(center)
```