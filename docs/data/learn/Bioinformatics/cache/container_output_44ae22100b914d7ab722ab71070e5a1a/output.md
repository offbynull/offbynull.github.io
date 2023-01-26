`{bm-disable-all}`[ch10_code/src/hmm/EmpiricalLearning.py](ch10_code/src/hmm/EmpiricalLearning.py) (lines 293 to 337):`{bm-enable-all}`

```python
def derive_hmm_structure(
        observed_sequence: list[tuple[STATE, STATE, SYMBOL] | tuple[STATE, STATE]]
) -> tuple[
    dict[STATE, set[STATE]],  # hidden state-hidden state transitions
    dict[STATE, set[SYMBOL]]  # hidden state-symbol emission transitions
]:
    symbols = set()
    emitting_hidden_states = set()
    non_emitting_hidden_states = set()
    # Walk entries in observed sequence
    for entry in observed_sequence:
        if len(entry) == 3:
            from_state, to_state, to_symbol = entry
            symbols.add(to_symbol)
            emitting_hidden_states.add(to_state)
        else:
            from_state, to_state = entry
            non_emitting_hidden_states.add(to_state)
    # Unable to infer when there are non-emitting hidden states. Recall that non-emitting hidden states cannot form
    # cycles because those cycles will infinitely blow out when exploding out an HMM (Viterbi). When there's only one
    # non-emitting hidden state, it's fine so long as you kill the edge to itself. When there's more than one
    # non-emitting hidden state, this algorithm assumes that they can point at each other, which will cause a cycle.
    #
    # For example, if there are two non-emitting states A and B, this algorithm will always produce a cycle.
    # .----.
    # |    v
    # A<---B
    #
    # The observed sequence doesn't make it clear which of thw two edges should be kept vs which should be discarded. As
    # such, non-emitting hidden states (other than the SOURCE state) aren't allowed in this algorithm.
    if non_emitting_hidden_states:
        raise ValueError('Cannot derive HMM structure when there are non-emitting hidden sates')
    # Assume first transition always begins from the SOURCE hidden state -- add it as non-emitting hidden state
    source_state = observed_sequence[0][0]
    # Build out HMM structure
    transitions = {}
    transitions[source_state] = emitting_hidden_states.copy()
    for state in emitting_hidden_states:
        transitions[state] = emitting_hidden_states.copy()
    emissions = {}
    emissions[source_state] = {}
    for state in emitting_hidden_states:
        emissions[state] = symbols.copy()
    return transitions, emissions
```