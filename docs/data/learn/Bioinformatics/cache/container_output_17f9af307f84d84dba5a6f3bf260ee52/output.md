```python
def find_closest_center(
        point: tuple[float],
        centers: list[tuple[float]],
) -> tuple[tuple[float], float]:
    center = min(
        centers,
        key=lambda cp: dist(point, cp)
    )
    return center, dist(center, point)
```