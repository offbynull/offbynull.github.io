```python
# For each center, estimate the confidence of point belonging to that center using the partition
# function from statistical physics.
#
# What is the partition function's stiffness parameter? You can thnk of stiffness as how willing
# the partition function is to be polarizing. For example, if you set stiffness to 1.0, whichever
# center the point teeters towards will have maximum confidence (1) while all other centers will
# have no confidence (0).
def confidence(
        point: tuple[float],
        centers: list[tuple[float]],
        stiffness: float
) -> dict[tuple[float], float]:
    confidences = {}
    total = 0
    for c in centers:
        total += e ** (-stiffness * dist(point, c))
    for c in centers:
        val = e ** (-stiffness * dist(point, c))
        confidences[c] = val / total
    return confidences  # center -> confidence value


# E-STEP: For each data point, estimate the confidence level of it belonging to each of the
# centers.
def e_step(
        points: list[tuple[float]],
        centers: list[tuple[float]],
        stiffness: float
) -> MembershipConfidenceMap:
    membership_confidence = {c: {} for c in centers}
    for pt in points:
        pt_confidences = confidence(pt, centers, stiffness)
        for c, val in pt_confidences.items():
            membership_confidence[c][pt] = val
    return membership_confidence  # confidence per (center, point) pair
```