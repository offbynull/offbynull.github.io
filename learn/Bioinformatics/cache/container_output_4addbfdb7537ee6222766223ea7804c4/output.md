`{bm-disable-all}`[ch10_code/src/hmm/BaumWelchLearning.py](ch10_code/src/hmm/BaumWelchLearning.py) (lines 18 to 57):`{bm-enable-all}`

```python
from hmm.ViterbiLearning import randomize_hmm_probabilities


def baum_welch_learning(
        hmm: Graph[STATE, HmmNodeData, TRANSITION, HmmEdgeData],
        hmm_source_n_id: STATE,
        hmm_sink_n_id: STATE,
        emitted_seq: list[SYMBOL],
        pseudocount: float,
        cycles: int
) -> Generator[
    tuple[
        Graph[STATE, HmmNodeData, TRANSITION, HmmEdgeData],
        dict[tuple[STATE, STATE], float],
        dict[tuple[STATE, SYMBOL], float]
    ],
    None,
    None
]:
    for _ in range(cycles):
        transition_probs = edge_certainties_to_transition_probabilities(hmm, hmm_sink_n_id, hmm_source_n_id, emitted_seq)
        emission_probs = node_certainties_to_emission_probabilities(hmm, hmm_sink_n_id, hmm_source_n_id, emitted_seq)
        # Apply new probabilities
        for (hmm_from_n_id, hmm_to_n_id), prob in transition_probs.items():
            transition = hmm_from_n_id, hmm_to_n_id
            hmm.get_edge_data(transition).set_transition_probability(prob)
        for (hmm_to_n_id, symbol), prob in emission_probs.items():
            hmm.get_node_data(hmm_to_n_id).set_symbol_emission_probability(symbol, prob)
        # Apply pseudocounts to new probabilities
        hmm_add_pseudocounts_to_hidden_state_transition_probabilities(
            hmm,
            pseudocount
        )
        hmm_add_pseudocounts_to_symbol_emission_probabilities(
            hmm,
            pseudocount
        )
        # Yield
        yield hmm, transition_probs, emission_probs
```