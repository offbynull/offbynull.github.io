```python
def partition_function(
        point: tuple[float],
        center_pts: list[tuple[float]],
        stiffness: float
):
    confidences = {}
    total_pf = 0
    for c_pt in center_pts:
        total_pf += e ** (-stiffness * dist(point, c_pt))
    for c_pt in center_pts:
        pf = e ** (-stiffness * dist(point, c_pt))
        confidences[point] = pf / total_pf
    return confidences
```