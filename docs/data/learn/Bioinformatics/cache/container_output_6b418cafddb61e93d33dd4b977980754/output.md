`{bm-disable-all}`[ch10_code/src/hmm/MostProbableHiddenPath_Viterbi.py](ch10_code/src/hmm/MostProbableHiddenPath_Viterbi.py) (lines 251 to 279):`{bm-enable-all}`

```python
def max_product_path_in_viterbi(
        viterbi: Graph[VITERBI_NODE_ID, Any, VITERBI_EDGE_ID, float]
):
    # Backtrack to find path with max sum -- using logged weights, path with max sum is actually path with max product.
    # Note that the call to populate_weights_and_backtrack_pointers() below is taking the math.log() of the edge weight
    # rather than passing back the edge weight itself.
    source_n_id = viterbi.get_root_node()
    sink_n_id = viterbi.get_leaf_node()
    FindMaxPath_DPBacktrack.populate_weights_and_backtrack_pointers(
        viterbi,
        source_n_id,
        lambda n, w, e: viterbi.update_node_data(n, (w, e)),
        lambda n: viterbi.get_node_data(n),
        lambda e: -math.inf if viterbi.get_edge_data(e) == 0 else math.log(viterbi.get_edge_data(e)),
    )
    edges = FindMaxPath_DPBacktrack.backtrack(
        viterbi,
        sink_n_id,
        lambda n_id: viterbi.get_node_data(n_id)
    )
    path = []
    final_weight = 1.0
    for e_id in edges:
        _, from_node = viterbi.get_edge_from(e_id)
        _, to_node = viterbi.get_edge_to(e_id)
        path.append((from_node, to_node))
        weight = viterbi.get_edge_data(e_id)
        final_weight *= weight
    return final_weight, path
```