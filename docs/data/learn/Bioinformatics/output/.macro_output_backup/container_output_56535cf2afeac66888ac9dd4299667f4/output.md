`{bm-disable-all}`[ch7_code/src/simple_tree_tester/SimpleTreeTester.py](ch7_code/src/simple_tree_tester/SimpleTreeTester.py) (lines 12 to 52):`{bm-enable-all}`

```python
def is_simple_tree(g: Graph[N, ND, E, float]) -> bool:
    # Check for cycles
    if len(g) == 0:
        return False
    walked_edges = set()
    walked_nodes = set()
    queued_edges = set()
    start_n = next(g.get_nodes())
    for e in g.get_outputs(start_n):
        queued_edges.add((start_n, e))
    while len(queued_edges) > 0:
        ignore_n, e = queued_edges.pop()
        active_n = [n for n in g.get_edge_ends(e) if n != ignore_n][0]
        walked_edges.add(e)
        walked_nodes.update({ignore_n, active_n})
        children = set(g.get_outputs(active_n))
        children.remove(e)
        for child_e in children:
            if child_e in walked_edges:
                return False  # cyclic -- edge already walked
            child_ignore_n = active_n
            queued_edges.add((child_ignore_n, child_e))
    # Check for disconnected graph
    if len(walked_nodes) != len(g):
        return False  # disconnected -- some nodes not reachable
    # Test degrees
    for n in g.get_nodes():
        # Degree == 1 is leaf node
        # Degree == 2 is a non-splitting internal node (NOT ALLOWED)
        # Degree > 2 is splitting internal node
        degree = g.get_degree(n)
        if degree == 2:
            return False
    # Test weights
    for e in g.get_edges():
        # No non-positive weights
        weight = g.get_edge_data(e)
        if weight <= 0:
            return False
    return True
```