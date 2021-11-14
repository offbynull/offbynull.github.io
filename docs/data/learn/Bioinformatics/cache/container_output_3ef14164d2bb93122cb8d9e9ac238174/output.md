`{bm-disable-all}`[ch7_code/src/sequence_phylogeny/SmallParsimony.py](ch7_code/src/sequence_phylogeny/SmallParsimony.py) (lines 150 to 183):`{bm-enable-all}`

```python
def distance_for_internal_element_types(
        downstream_dist_sets: Iterable[dict[str, float]],
        dist_metric: Callable[[str, str], float],
        elem_types: str = 'ACTG'
) -> dict[str, float]:
    dist_set = {}
    for elem_type in elem_types:
        dist = distance_for_internal_element_type(
            downstream_dist_sets,
            dist_metric,
            elem_type,
            elem_types
        )
        dist_set[elem_type] = dist
    return dist_set


def distance_for_internal_element_type(
        downstream_dist_sets: Iterable[dict[str, float]],
        dist_metric: Callable[[str, str], float],
        elem_type_dst: str,
        elem_types: str = 'ACTG'
) -> float:
    min_dists = []
    for downstream_dist_set in downstream_dist_sets:
        possible_dists = []
        for elem_type_src in elem_types:
            downstream_dist = downstream_dist_set[elem_type_src]
            transition_cost = dist_metric(elem_type_src, elem_type_dst)
            dist = downstream_dist + transition_cost
            possible_dists.append(dist)
        min_dist = min(possible_dists)
        min_dists.append(min_dist)
    return sum(min_dists)
```