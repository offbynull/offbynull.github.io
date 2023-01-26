`{bm-disable-all}`[ch10_code/src/hmm/MostProbableHiddenPath_ViterbiNonEmittingHiddenStates.py](ch10_code/src/hmm/MostProbableHiddenPath_ViterbiNonEmittingHiddenStates.py) (lines 114 to 219):`{bm-enable-all}`

```python
VITERBI_NODE_ID = tuple[int, STATE]
VITERBI_EDGE_ID = tuple[VITERBI_NODE_ID, VITERBI_NODE_ID]


def to_viterbi_graph(
        hmm: Graph[STATE, HmmNodeData, TRANSITION, HmmEdgeData],
        hmm_source_n_id: STATE,
        hmm_sink_n_id: STATE,
        emissions: list[SYMBOL]
) -> Graph[VITERBI_NODE_ID, Any, VITERBI_EDGE_ID, float]:
    viterbi = Graph()
    # Add Viterbi source node.
    viterbi_source_n_id = -1, hmm_source_n_id
    viterbi.insert_node(viterbi_source_n_id)
    # Explode out HMM into Viterbi.
    viterbi_from_n_emissions_idx = -1
    viterbi_from_n_ids = {viterbi_source_n_id}
    viterbi_to_n_emissions_idx = 0
    viterbi_to_n_ids_emitting = set()
    viterbi_to_n_ids_non_emitting = set()
    while viterbi_from_n_ids and viterbi_to_n_emissions_idx < len(emissions):
        viterbi_to_n_symbol = emissions[viterbi_to_n_emissions_idx]
        viterbi_to_n_ids_emitting = set()
        viterbi_to_n_ids_non_emitting = set()
        while viterbi_from_n_ids:
            viterbi_from_n_id = viterbi_from_n_ids.pop()
            _, hmm_from_n_id = viterbi_from_n_id
            for _, _, hmm_to_n_id, _ in hmm.get_outputs_full(hmm_from_n_id):
                hmm_to_n_emittable = hmm.get_node_data(hmm_to_n_id).is_emittable()
                transition = hmm_from_n_id, hmm_to_n_id
                if hmm_to_n_emittable:
                    hidden_state_transition_prob = hmm.get_edge_data(transition).get_transition_probability()
                    symbol_emission_prob = hmm.get_node_data(hmm_to_n_id).get_symbol_emission_probability(viterbi_to_n_symbol)
                    viterbi_to_n_id = viterbi_to_n_emissions_idx, hmm_to_n_id
                    connect_viterbi_nodes(
                        viterbi,
                        viterbi_from_n_id,
                        viterbi_to_n_id,
                        hidden_state_transition_prob * symbol_emission_prob
                    )
                    viterbi_to_n_ids_emitting.add(viterbi_to_n_id)
                else:
                    hidden_state_transition_prob =  hmm.get_edge_data(transition).get_transition_probability()
                    viterbi_to_n_id = viterbi_from_n_emissions_idx, hmm_to_n_id
                    to_n_existed = connect_viterbi_nodes(
                        viterbi,
                        viterbi_from_n_id,
                        viterbi_to_n_id,
                        hidden_state_transition_prob
                    )
                    if not to_n_existed:
                        viterbi_from_n_ids.add(viterbi_to_n_id)
                    viterbi_to_n_ids_non_emitting.add(viterbi_to_n_id)
        viterbi_from_n_ids = viterbi_to_n_ids_emitting
        viterbi_from_n_emissions_idx += 1
        viterbi_to_n_emissions_idx += 1
    # Ensure all emitted symbols were consumed when exploding out to Viterbi.
    assert viterbi_to_n_emissions_idx == len(emissions)
    # Explode out the non-emitting hidden states of the final last emission index (does not happen in the above loop).
    viterbi_to_n_ids_non_emitting = set()
    viterbi_from_n_ids = viterbi_to_n_ids_emitting.copy()
    while viterbi_from_n_ids:
        viterbi_from_n_id = viterbi_from_n_ids.pop()
        _, hmm_from_n_id = viterbi_from_n_id
        for _, _, hmm_to_n_id, _ in hmm.get_outputs_full(hmm_from_n_id):
            hmm_to_n_emmitable = hmm.get_node_data(hmm_to_n_id).is_emittable()
            if hmm_to_n_emmitable:
                continue
            transition = hmm_from_n_id, hmm_to_n_id
            hidden_state_transition_prob = hmm.get_edge_data(transition).get_transition_probability()
            viterbi_to_n_id = viterbi_from_n_emissions_idx, hmm_to_n_id
            connect_viterbi_nodes(
                viterbi,
                viterbi_from_n_id,
                viterbi_to_n_id,
                hidden_state_transition_prob
            )
            viterbi_to_n_ids_non_emitting.add(viterbi_to_n_id)
            viterbi_from_n_ids.add(viterbi_to_n_id)
    # Add Viterbi sink node.
    viterbi_to_n_id = -1, hmm_sink_n_id
    for viterbi_from_n_id in viterbi_to_n_ids_emitting | viterbi_to_n_ids_non_emitting:
        connect_viterbi_nodes(viterbi, viterbi_from_n_id, viterbi_to_n_id, 1.0)
    return viterbi


def connect_viterbi_nodes(
        viterbi: Graph[VITERBI_NODE_ID, Any, VITERBI_EDGE_ID, float],
        viterbi_from_n_id: VITERBI_NODE_ID,
        viterbi_to_n_id: VITERBI_NODE_ID,
        weight: float
) -> bool:
    to_n_existed = True
    if not viterbi.has_node(viterbi_to_n_id):
        viterbi.insert_node(viterbi_to_n_id)
        to_n_existed = False
    viterbi_e_weight = weight
    viterbi_e_id = viterbi_from_n_id, viterbi_to_n_id
    viterbi.insert_edge(
        viterbi_e_id,
        viterbi_from_n_id,
        viterbi_to_n_id,
        viterbi_e_weight
    )
    return to_n_existed
```