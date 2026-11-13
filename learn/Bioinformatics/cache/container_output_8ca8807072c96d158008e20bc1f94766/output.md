`{bm-disable-all}`[ch3_code/src/WalkRandomEulerianCycle.py](ch3_code/src/WalkRandomEulerianCycle.py) (lines 14 to 64):`{bm-enable-all}`

```python
# (6, 8), (8, 7), (7, 9), (9, 6)  ---->  68796
def edge_list_to_node_list(edges: List[Tuple[T, T]]) -> List[T]:
    ret = [edges[0][0]]
    for e in edges:
        ret.append(e[1])
    return ret


def randomly_walk_and_remove_edges_until_cycle(graph: Graph[T], node: T) -> List[T]:
    end_node = node
    edge_list = []
    from_node = node
    while len(graph) > 0:
        to_nodes = graph.get_outputs(from_node)
        to_node = next(to_nodes, None)
        assert to_node is not None  # eularian graphs are strongly connected, meaning we should never hit dead-end nodes

        graph.delete_edge(from_node, to_node, True, True)

        edge = (from_node, to_node)
        edge_list.append(edge)
        from_node = to_node
        if from_node == end_node:
            return edge_list_to_node_list(edge_list)

    assert False  # eularian graphs are strongly connected and balanced, meaning we should never run out of nodes


# graph must be strongly connected
# graph must be balanced
# if the 2 conditions above are met, the graph will be eularian (a eulerian cycle exists)
def walk_eulerian_cycle(graph: Graph[T], start_node: T) -> List[T]:
    graph = graph.copy()

    node_cycle = randomly_walk_and_remove_edges_until_cycle(graph, start_node)
    node_cycle_ptr = 0
    while len(graph) > 0:
        new_node_cycle = None
        for local_ptr, node in enumerate(node_cycle[node_cycle_ptr:]):
            if node not in graph:
                continue
            node_cycle_ptr += local_ptr
            inject_node_cycle = randomly_walk_and_remove_edges_until_cycle(graph, node)
            new_node_cycle = node_cycle[:]
            new_node_cycle[node_cycle_ptr:node_cycle_ptr+1] = inject_node_cycle
            break
        assert new_node_cycle is not None
        node_cycle = new_node_cycle

    return node_cycle
```