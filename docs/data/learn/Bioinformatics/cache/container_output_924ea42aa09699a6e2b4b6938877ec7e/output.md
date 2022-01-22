```python
def weighted_center_of_gravity(
        confidence_set: dict[tuple[float], float],
        dims: int
) -> tuple[float]:
    center_pt: list[float] = []
    for i in range(dims):
        pt_coordinates = [pt[i] for pt in confidence_set.keys()]
        pt_confidences = confidence_set.values()
        total_confidences = sum(pt_confidences)
        ct_coordinate = dot_product(pt_coordinates, pt_confidences) / total_confidences
        center_pt.append(ct_coordinate)
    return tuple(center_pt)
```