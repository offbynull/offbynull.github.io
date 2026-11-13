`{bm-disable-all}`[ch10_code/src/hmm/ProbabilityOfEmittedSequenceWhereHiddenPathTravelsThroughEdge_Summation.py](ch10_code/src/hmm/ProbabilityOfEmittedSequenceWhereHiddenPathTravelsThroughEdge_Summation.py) (lines 13 to 92):`{bm-enable-all}`

```python
def enumerate_paths_targeting_transition_after_index(
        hmm: Graph[STATE, HmmNodeData, TRANSITION, HmmEdgeData],
        hmm_from_n_id: STATE,
        emitted_seq_len: int,
        from_emission_idx: int,
        from_hidden_state: STATE,
        to_hidden_state: STATE,
        prev_path: list[TRANSITION] | None = None,
        emission_idx: int = 0
) -> Generator[list[TRANSITION], None, None]:
    if prev_path is None:
        prev_path = []
    if emission_idx == emitted_seq_len:
        # We're at the end of the expected emitted sequence length, so return the current path. However, at this point
        # hmm_from_n_id may still have transitions to other non-emittable hidden states, and so those need to be
        # returned as paths as well (continue digging into outgoing transitions if the destination is non-emittable).
        yield prev_path
        for transition, hmm_from_n_id, hmm_to_n_id, _ in hmm.get_outputs_full(hmm_from_n_id):
            if hmm.get_node_data(hmm_to_n_id).is_emittable():
                continue
            if emission_idx == from_emission_idx + 1 and (hmm_from_n_id != from_hidden_state or hmm_to_n_id != to_hidden_state):
                continue
            prev_path.append(transition)
            yield from enumerate_paths_targeting_transition_after_index(hmm, hmm_to_n_id, emitted_seq_len,
                                                                        from_emission_idx, from_hidden_state,
                                                                        to_hidden_state, prev_path, emission_idx)
            prev_path.pop()
    else:
        # Explode out at that path by digging into transitions from hmm_from_n_id. When at from_emission_idx, only take
        # the transition from_hidden_state->to_hidden_state.
        for transition, hmm_from_n_id, hmm_to_n_id, _ in hmm.get_outputs_full(hmm_from_n_id):
            if emission_idx == from_emission_idx + 1 and (hmm_from_n_id != from_hidden_state or hmm_to_n_id != to_hidden_state):
                continue
            prev_path.append(transition)
            if hmm.get_node_data(hmm_to_n_id).is_emittable():
                next_emission_idx = emission_idx + 1
            else:
                next_emission_idx = emission_idx
            yield from enumerate_paths_targeting_transition_after_index(hmm, hmm_to_n_id, emitted_seq_len,
                                                                        from_emission_idx, from_hidden_state,
                                                                        to_hidden_state, prev_path, next_emission_idx)
            prev_path.pop()


def emission_probability(
        hmm: Graph[STATE, HmmNodeData, TRANSITION, HmmEdgeData],
        hmm_source_n_id: STATE,
        emitted_seq: list[SYMBOL],
        from_emission_idx: int,
        from_hidden_state: STATE,
        to_hidden_state: STATE,
) -> float:
    path_iterator = enumerate_paths_targeting_transition_after_index(
        hmm,
        hmm_source_n_id,
        len(emitted_seq),
        from_emission_idx,
        from_hidden_state,
        to_hidden_state
    )
    isolated_probs_sum = 0.0
    for path in path_iterator:
        isolated_probs_sum += probability_of_transitions_and_emissions(hmm, path, emitted_seq)
    return isolated_probs_sum


def probability_of_transitions_and_emissions(hmm, path, emitted_seq):
    emitted_seq_idx = 0
    prob = 1.0
    for transition in path:
        hmm_from_n_id, hmm_to_n_id = transition
        if hmm.get_node_data(hmm_to_n_id).is_emittable():
            symbol = emitted_seq[emitted_seq_idx]
            prob *= hmm.get_node_data(hmm_to_n_id).get_symbol_emission_probability(symbol) * \
                    hmm.get_edge_data(transition).get_transition_probability()
            emitted_seq_idx += 1
        else:
            prob *= hmm.get_edge_data(transition).get_transition_probability()
    return prob
```