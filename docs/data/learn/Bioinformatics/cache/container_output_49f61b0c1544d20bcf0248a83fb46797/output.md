`{bm-disable-all}`[ch7_code/src/phylogeny/UPGMA.py](ch7_code/src/phylogeny/UPGMA.py) (lines 74 to 143):`{bm-enable-all}`

```python
def find_clusters_with_min_dist(dm: DistanceMatrix[N], c_set: ClusterSet) -> tuple[N, N, float]:
    assert c_set.active_count() > 1
    min_n1_id = None
    min_n2_id = None
    min_dist = None
    for n1, n2 in product(c_set.active(), repeat=2):
        if n1 == n2:
            continue
        d = dm[n1, n2]
        if min_dist is None or d < min_dist:
            min_n1_id = n1
            min_n2_id = n2
            min_dist = d
    assert min_n1_id is not None and min_n2_id is not None and min_dist is not None
    return min_n1_id, min_n2_id, min_dist


def cluster_merge(
        dm: DistanceMatrix[N],
        dm_orig: DistanceMatrix[N],
        c_set: ClusterSet,
        old_id1: N,
        old_id2: N,
        new_id: N
) -> None:
    c_set.merge(new_id, old_id1, old_id2)  # create new cluster w/ elements from old - old_ids deactived+new_id actived
    new_dists = {}
    for existing_id in dm.leaf_ids():
        if existing_id == old_id1 or existing_id == old_id2:
            continue
        new_dist = cluster_dist(dm_orig, c_set, new_id, existing_id)
        new_dists[existing_id] = new_dist
    dm.merge(new_id, old_id1, old_id2, new_dists)  # remove old ids and replace with new_id that has new distances


def upgma(dm: DistanceMatrix[N]) -> tuple[Graph, N]:
    g = Graph()
    c_set = ClusterSet(dm)  # primed with leaf nodes (all active)
    for node in dm.leaf_ids_it():
        g.insert_node(node, 0)  # initial node weights (each leaf node has an age of 0)
    dm_orig = dm.copy()
    # set node ages
    next_node_id = 0
    next_edge_id = 0
    while c_set.active_count() > 1:
        min_n1_id, min_n2_id, min_dist = find_clusters_with_min_dist(dm, c_set)
        new_node_id = next_node_id
        new_node_age = min_dist / 2
        g.insert_node(f'C{new_node_id}', new_node_age)
        next_node_id += 1
        g.insert_edge(f'E{next_edge_id}', min_n1_id, f'C{new_node_id}')
        next_edge_id += 1
        g.insert_edge(f'E{next_edge_id}', min_n2_id, f'C{new_node_id}')
        next_edge_id += 1
        cluster_merge(dm, dm_orig, c_set, min_n1_id, min_n2_id, f'C{new_node_id}')
    # set amount of age added by each edge
    nodes_by_age = sorted([(n, g.get_node_data(n)) for n in g.get_nodes()], key=lambda x: x[1])
    set_edges = set()  # edges that have already had their weights set
    for child_n, child_age in nodes_by_age:
        for e in g.get_outputs(child_n):
            if e in set_edges:
                continue
            parent_n = [n for n in g.get_edge_ends(e) if n != child_n].pop()
            parent_age = g.get_node_data(parent_n)
            weight = parent_age - child_age
            g.update_edge_data(e, weight)
            set_edges.add(e)
    root_id = c_set.active().pop()
    return g, root_id
```