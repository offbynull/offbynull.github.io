`{bm-disable-all}`[ch10_code/src/hmm/ProbabilityOfEmittedSequence_Naive.py](ch10_code/src/hmm/ProbabilityOfEmittedSequence_Naive.py) (lines 108 to 166):`{bm-enable-all}`

```python
def enumerate_paths(
        hmm: Graph[N, ND, E, ED],
        hmm_from_n_id: N,
        emitted_seq_len: int,
        get_node_emittable: Callable[[Graph[N, ND, E, ED], STATE], bool],
        prev_path: list[E] | None = None
) -> Generator[list[E], None, None]:
    if prev_path is None:
        prev_path = []
    if emitted_seq_len == 0:
        # We're at the end of the expected emitted sequence length, so return the current path. However, at this point
        # hmm_from_n_id may still have transitions to other non-emittable hidden states, and so those need to be
        # returned as paths as well (continue digging into outgoing transitions if the destination is non-emittable).
        yield prev_path
        for hmm_e_id, _, hmm_to_n_id, transition_prob in hmm.get_outputs_full(hmm_from_n_id):
            if get_node_emittable(hmm, hmm_to_n_id):
                continue
            prev_path.append(hmm_e_id)
            yield from enumerate_paths(hmm, hmm_to_n_id, emitted_seq_len, get_node_emittable, prev_path)
            prev_path.pop()
    else:
        # Explode out at that path by digging into transitions from hmm_from_n_id. If the destination of the transition
        # is an ...
        # * emittable hidden state, subtract the expected emitted sequence length by 1 when you dig down.
        # * non-emittable hidden state, keep the expected emitted sequence length the same when you dig down.
        for hmm_e_id, _, hmm_to_n_id, transition_prob in hmm.get_outputs_full(hmm_from_n_id):
            prev_path.append(hmm_e_id)
            if get_node_emittable(hmm, hmm_to_n_id):
                next_emittable_seq_len = emitted_seq_len - 1
            else:
                next_emittable_seq_len = emitted_seq_len
            yield from enumerate_paths(hmm, hmm_to_n_id, next_emittable_seq_len, get_node_emittable, prev_path)
            prev_path.pop()


def emission_probability(
        hmm: Graph[N, ND, E, ED],
        hmm_source_n_id: N,
        emitted_seq: list[SYMBOL],
        get_node_emission_prob: Callable[[Graph[N, ND, E, ED], STATE, SYMBOL], float],
        get_node_emittable: Callable[[Graph[N, ND, E, ED], STATE], bool],
        get_edge_transition_prob: Callable[[Graph[N, ND, E, ED], STATE, STATE], float]
):
    sum_of_probs = 0.0
    for p in enumerate_paths(hmm, hmm_source_n_id, len(emitted_seq), get_node_emittable):
        emitted_seq_idx = 0
        prob = 1.0
        for e_id in p:
            hmm_from_n_id, hmm_to_n_id, transition_prob = hmm.get_edge(e_id)
            if get_node_emittable(hmm, hmm_to_n_id):
                symbol = emitted_seq[emitted_seq_idx]
                prob *= get_node_emission_prob(hmm, hmm_to_n_id, symbol) *\
                        get_edge_transition_prob(hmm, hmm_from_n_id, hmm_to_n_id)
                emitted_seq_idx += 1
            else:
                prob *= get_edge_transition_prob(hmm, hmm_from_n_id, hmm_to_n_id)
        sum_of_probs += prob
    return sum_of_probs
```