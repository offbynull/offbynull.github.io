```python
def walk_until_distance(
        tree: Graph[N, ND, E, float],
        n_start: N,
        n_end: N,
        dist: float
) -> Union[
    tuple[Literal['NODE'], N],
    tuple[Literal['EDGE'], E, N, N, float, float]
]:
    path = find_path(tree, n_start, n_end)
    last_edge_end = n_start
    dist_walked = 0.0
    for edge in path:
        ends = tree.get_edge_ends(edge)
        n1 = last_edge_end
        n2 = next(n for n in ends if n != last_edge_end)
        weight = tree.get_edge_data(edge)
        dist_walked_with_weight = dist_walked + weight
        if dist_walked_with_weight > dist:
            return 'EDGE', edge, n1, n2, dist_walked, weight
        elif dist_walked_with_weight == dist:
            return 'NODE', n2
        dist_walked = dist_walked_with_weight
        last_edge_end = n2
    raise ValueError('Bad inputs')
```