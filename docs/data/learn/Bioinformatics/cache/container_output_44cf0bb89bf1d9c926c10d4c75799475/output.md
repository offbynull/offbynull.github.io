```python
def k_means_soft_lloyds(
        k: int,
        points: list[tuple[float]],
        centers_init: list[tuple[float]],
        dims: int,
        stiffness: float,
        iteration_callback: IterationCallbackFunc
) -> MembershipConfidenceMap:
    centers = centers_init[:]
    while True:
        membership_confidences = e_step(points, centers, stiffness)  # step1: centers to clusters (E-step)
        centers = m_step(membership_confidences, dims)               # step2: clusters to centers (M-step)
        # check to see if you can stop iterating ("converged" enough to stop)
        continue_flag = iteration_callback(membership_confidences)
        if not continue_flag:
            break
    return membership_confidences
```