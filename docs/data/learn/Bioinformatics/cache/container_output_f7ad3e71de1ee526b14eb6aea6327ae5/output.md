```python
def weighted_center_of_gravity(
        confidence_set: dict[tuple[float], float],
        dims: int
) -> tuple[float]:
    center: list[float] = []
    all_confidences = confidence_set.values()
    all_confidences_summed = sum(all_confidences)
    for i in range(dims):
        val = 0.0
        for pt, confidence in confidence_set.items():
            val += pt[i] * confidence  # scale by confidence
        val /= all_confidences_summed
        center.append(val)
    return tuple(center)


# M-STEP: Calculate a new set of centers from the "confidence levels" derived in the E-step.
def m_step(
        membership_confidences: MembershipConfidenceMap,
        dims: int
) -> list[tuple[float]]:
    centers = []
    for c in membership_confidences:
        new_c = weighted_center_of_gravity(
            membership_confidences[c],
            dims
        )
        centers.append(new_c)
    return centers
```