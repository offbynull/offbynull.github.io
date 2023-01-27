`{bm-disable-all}`[ch10_code/src/hmm/ProbabilityOfEmittedSequenceWithIndexEmittingFromHiddenState_Naive.py](ch10_code/src/hmm/ProbabilityOfEmittedSequenceWithIndexEmittingFromHiddenState_Naive.py) (lines 147 to 241):`{bm-enable-all}`

```python
def enumerate_paths_targeting_hidden_state_at_index(
        hmm: Graph[STATE, HmmNodeData, TRANSITION, HmmEdgeData],
        hmm_from_n_id: STATE,
        emitted_seq_len: int,
        emitted_seq_idx_of_interest: int,
        hidden_state_of_interest: STATE,
        prev_path: list[TRANSITION] | None = None
) -> Generator[list[TRANSITION], None, None]:
    if prev_path is None:
        prev_path = []
    if emitted_seq_len == 0:
        # We're at the end of the expected emitted sequence length, so return the current path. However, at this point
        # hmm_from_n_id may still have transitions to other non-emittable hidden states, and so those need to be
        # returned as paths as well (continue digging into outgoing transitions if the destination is non-emittable).
        yield prev_path
        for transition, _, hmm_to_n_id, _ in hmm.get_outputs_full(hmm_from_n_id):
            if hmm.get_node_data(hmm_to_n_id).is_emittable():
                continue
            prev_path.append(transition)
            yield from enumerate_paths_targeting_hidden_state_at_index(hmm, hmm_to_n_id, emitted_seq_len, emitted_seq_idx_of_interest,
                                                                       hidden_state_of_interest, prev_path)
            prev_path.pop()
    else:
        # About to explode out by digging into transitions from hmm_from_n_id. But, before doing that, check if this is
        # emitted sequence index that's being isolated. If it is, we want to isolate things such that we only travel
        # down the hidden state of interest.
        if emitted_seq_idx_of_interest != 0:
            outputs = list(hmm.get_outputs_full(hmm_from_n_id))
        else:
            outputs = []
            for transition, hmm_from_n_id, hmm_to_n_id, transition_data in hmm.get_outputs_full(hmm_from_n_id):
                if hmm_to_n_id == hidden_state_of_interest or not hmm.get_node_data(hmm_to_n_id).is_emittable():
                    outputs.append((transition, hmm_from_n_id, hmm_to_n_id, transition_data))
        # Explode out at that path by digging into transitions from hmm_from_n_id. If the destination of the transition
        # is an ...
        # * emittable hidden state, subtract the expected emitted sequence length by 1 when you dig down.
        # * non-emittable hidden state, keep the expected emitted sequence length the same when you dig down.
        for transition, _, hmm_to_n_id, _ in outputs:
            prev_path.append(transition)
            if hmm.get_node_data(hmm_to_n_id).is_emittable():
                next_emittable_seq_len = emitted_seq_len - 1
                next_emitted_seq_idx_of_interest = emitted_seq_idx_of_interest - 1
            else:
                next_emittable_seq_len = emitted_seq_len
                next_emitted_seq_idx_of_interest = emitted_seq_idx_of_interest
            yield from enumerate_paths_targeting_hidden_state_at_index(hmm, hmm_to_n_id, next_emittable_seq_len,
                                                                       next_emitted_seq_idx_of_interest, hidden_state_of_interest, prev_path)
            prev_path.pop()


def emission_probability(
        hmm: Graph[STATE, HmmNodeData, TRANSITION, HmmEdgeData],
        hmm_source_n_id: STATE,
        emitted_seq: list[SYMBOL],
        emitted_seq_idx_of_interest: int,
        hidden_state_of_interest: STATE
) -> float:
    # Calculate isolated
    path_iterator = enumerate_paths_targeting_hidden_state_at_index(
        hmm,
        hmm_source_n_id,
        len(emitted_seq),
        emitted_seq_idx_of_interest,
        hidden_state_of_interest
    )
    isolated_probs_sum = 0.0
    for path in path_iterator:
        isolated_probs_sum += probability_of_transitions_and_emissions(hmm, path, emitted_seq)
    # Calculate full - This is using enumerate_paths from the original ProbabilityOfEmittedSequence_Naive
    path_iterator = enumerate_paths(
        hmm,
        hmm_source_n_id,
        len(emitted_seq)
    )
    full_probs_sum = 0.0
    for path in path_iterator:
        full_probs_sum += probability_of_transitions_and_emissions(hmm, path, emitted_seq)
    # Return probability
    return isolated_probs_sum / full_probs_sum


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