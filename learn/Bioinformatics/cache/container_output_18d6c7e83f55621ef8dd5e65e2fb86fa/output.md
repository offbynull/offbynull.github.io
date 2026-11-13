`{bm-disable-all}`[ch5_code/src/find_max_path/FindMaxPath_DPCache.py](ch5_code/src/find_max_path/FindMaxPath_DPCache.py) (lines 21 to 56):`{bm-enable-all}`

```python
def find_max_path(
        graph: Graph[N, ND, E, ED],
        current_node: N,
        end_node: N,
        cache: Dict[N, Optional[Tuple[List[E], float]]],
        get_edge_weight_func: GET_EDGE_WEIGHT_FUNC_TYPE
) -> Optional[Tuple[List[E], float]]:
    if current_node == end_node:
        return [], 0.0
    alternatives = []
    for edge_id in graph.get_outputs(current_node):
        edge_weight = get_edge_weight_func(edge_id)
        child_n = graph.get_edge_to(edge_id)
        if child_n in cache:
            res = cache[child_n]
        else:
            res = find_max_path(
                graph,
                child_n,
                end_node,
                cache,
                get_edge_weight_func
            )
            cache[child_n] = res
        if res is None:
            continue
        path, weight = res
        path = [edge_id] + path
        weight = edge_weight + weight
        res = path, weight
        alternatives.append(res)
    if len(alternatives) == 0:
        return None  # no path to end, so return None
    else:
        return max(alternatives, key=lambda x: x[1])  # choose path to end with max weight
```