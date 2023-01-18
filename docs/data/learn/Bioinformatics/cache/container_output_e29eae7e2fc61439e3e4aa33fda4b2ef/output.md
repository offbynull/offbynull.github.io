`{bm-disable-all}`[ch10_code/src/hmm/ProbabilityOfEmittedSequence_Naive.py](ch10_code/src/hmm/ProbabilityOfEmittedSequence_Naive.py) (lines 108 to 148):`{bm-enable-all}`

```python
def enumerate_paths(
        hmm: Graph[N, ND, E, ED],
        hmm_from_n_id: N,
        emitted_seq_len: int,
        prev_path: list[E] | None = None
) -> Generator[list[E], None, None]:
    if emitted_seq_len == 0:
        yield prev_path
        return
    if prev_path is None:
        prev_path = []
    for hmm_e_id, _, hmm_to_n_id, transition_prob in hmm.get_outputs_full(hmm_from_n_id):
        prev_path.append(hmm_e_id)
        yield from enumerate_paths(hmm, hmm_to_n_id, emitted_seq_len - 1, prev_path)
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
    for p in enumerate_paths(hmm, hmm_source_n_id, len(emitted_seq)):
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