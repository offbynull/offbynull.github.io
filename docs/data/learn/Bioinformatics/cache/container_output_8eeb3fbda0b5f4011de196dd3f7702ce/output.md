`{bm-disable-all}`[ch10_code/src/hmm/ViterbiMostProbableHiddenPath_Standard.py](ch10_code/src/hmm/ViterbiMostProbableHiddenPath_Standard.py) (lines 33 to 84):`{bm-enable-all}`

```python
def to_viterbi_graph(
        hmm: Graph[N, ND, E, ED],
        hmm_source_n_id: N,
        hmm_sink_n_id: N,
        emissions: list[SYMBOL],
        get_node_emission_prob: Callable[[Graph[N, ND, E, ED], STATE, SYMBOL], float],
        get_edge_transition_prob: Callable[[Graph[N, ND, E, ED], STATE, STATE], float]
) -> Graph[tuple[int, N], Any, tuple[N, N], float]:
    viterbi = Graph()
    # Add Viterbi source node.
    viterbi_source_n_id = -1, hmm_source_n_id
    viterbi.insert_node(viterbi_source_n_id)
    # Explode out HMM into Viterbi.
    prev_nodes = {(hmm_source_n_id, viterbi_source_n_id)}
    emissions_idx = 0
    while prev_nodes and emissions_idx < len(emissions):
        symbol = emissions[emissions_idx]
        new_prev_nodes = set()
        for hmm_from_n_id, viterbi_from_n_id in prev_nodes:
            for _, _, hmm_to_n_id, _ in hmm.get_outputs_full(hmm_from_n_id):
                viterbi_to_n_id = emissions_idx, hmm_to_n_id
                if not viterbi.has_node(viterbi_to_n_id):
                    viterbi.insert_node(viterbi_to_n_id)
                    new_prev_nodes.add((hmm_to_n_id, viterbi_to_n_id))
                hidden_state_transition_prob = get_edge_transition_prob(hmm, hmm_from_n_id, hmm_to_n_id)
                symbol_emission_prob = get_node_emission_prob(hmm, hmm_to_n_id, symbol)
                viterbi_e_id = viterbi_from_n_id, viterbi_to_n_id
                viterbi_e_weight = hidden_state_transition_prob * symbol_emission_prob
                viterbi.insert_edge(
                    viterbi_e_id,
                    viterbi_from_n_id,
                    viterbi_to_n_id,
                    viterbi_e_weight
                )
        prev_nodes = new_prev_nodes
        emissions_idx += 1
    # Ensure all emitted symbols were consumed when exploding out to Viterbi.
    assert emissions_idx == len(emissions)
    # Add Viterbi sink node. Note that the HMM sink node ID doesn't have to exist in the HMM graph. It's only used to
    # represent a node in the Viterbi graph.
    viterbi_to_n_id = -1, hmm_sink_n_id
    viterbi.insert_node(viterbi_to_n_id)
    for hmm_from_n_id, viterbi_from_n_id in prev_nodes:
        viterbi_e_id = viterbi_from_n_id, viterbi_to_n_id
        viterbi_e_weight = 1.0
        viterbi.insert_edge(
            viterbi_e_id,
            viterbi_from_n_id,
            viterbi_to_n_id,
            viterbi_e_weight
        )
    return viterbi
```