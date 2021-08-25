`{bm-disable-all}`[ch3_code/src/WalkAllHamiltonianPaths.py](ch3_code/src/WalkAllHamiltonianPaths.py) (lines 15 to 38):`{bm-enable-all}`

```python
def exhaustively_walk_until_all_nodes_touched_exactly_one(
        graph: Graph[T],
        from_node: T,
        current_path: List[T]
) -> List[List[T]]:
    current_path.append(from_node)

    if len(current_path) == len(graph):
        found_paths = [current_path.copy()]
    else:
        found_paths = []
        for to_node in graph.get_outputs(from_node):
            if to_node in set(current_path):
                continue
            found_paths += exhaustively_walk_until_all_nodes_touched_exactly_one(graph, to_node, current_path)

    current_path.pop()
    return found_paths


# walk each node exactly once
def walk_hamiltonian_paths(graph: Graph[T], from_node: T) -> List[List[T]]:
    return exhaustively_walk_until_all_nodes_touched_exactly_one(graph, from_node, [])
```