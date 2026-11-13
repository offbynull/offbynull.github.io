`{bm-disable-all}`[ch10_code/src/hmm/ProbabilityOfEmittedSequence_Summation.py](ch10_code/src/hmm/ProbabilityOfEmittedSequence_Summation.py) (lines 14 to 69):`{bm-enable-all}`

```python
def enumerate_paths(
        hmm: Graph[STATE, HmmNodeData, TRANSITION, HmmEdgeData],
        hmm_from_n_id: STATE,
        emitted_seq_len: int,
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
        for transition, _, hmm_to_n_id, _ in hmm.get_outputs_full(hmm_from_n_id):
            if hmm.get_node_data(hmm_to_n_id).is_emittable():
                continue
            prev_path.append(transition)
            yield from enumerate_paths(hmm, hmm_to_n_id, emitted_seq_len, prev_path, emission_idx)
            prev_path.pop()
    else:
        # Explode out at that path by digging into transitions from hmm_from_n_id. If the destination of the transition
        # is an ...
        # * emittable hidden state, subtract the expected emitted sequence length by 1 when you dig down.
        # * non-emittable hidden state, keep the expected emitted sequence length the same when you dig down.
        for transition, _, hmm_to_n_id, _ in hmm.get_outputs_full(hmm_from_n_id):
            prev_path.append(transition)
            if hmm.get_node_data(hmm_to_n_id).is_emittable():
                next_emission_idx = emission_idx + 1
            else:
                next_emission_idx = emission_idx
            yield from enumerate_paths(hmm, hmm_to_n_id, emitted_seq_len, prev_path, next_emission_idx)
            prev_path.pop()


def emission_probability(
        hmm: Graph[STATE, HmmNodeData, TRANSITION, HmmEdgeData],
        hmm_source_n_id: STATE,
        emitted_seq: list[SYMBOL]
) -> float:
    sum_of_probs = 0.0
    for p in enumerate_paths(hmm, hmm_source_n_id, len(emitted_seq)):
        emitted_seq_idx = 0
        prob = 1.0
        for transition in p:
            hmm_from_n_id, hmm_to_n_id = transition
            if hmm.get_node_data(hmm_to_n_id).is_emittable():
                symbol = emitted_seq[emitted_seq_idx]
                prob *= hmm.get_node_data(hmm_to_n_id).get_symbol_emission_probability(symbol) *\
                        hmm.get_edge_data(transition).get_transition_probability()
                emitted_seq_idx += 1
            else:
                prob *= hmm.get_edge_data(transition).get_transition_probability()
        sum_of_probs += prob
    return sum_of_probs
```