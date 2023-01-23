`{bm-disable-all}`[ch10_code/src/hmm/EmpiricalLearning.py](ch10_code/src/hmm/EmpiricalLearning.py) (lines 263 to 298):`{bm-enable-all}`

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
    # Assume first transition always begins from the SOURCE hidden state -- add it as non-emitting hidden state
    source_state = observed_sequence[0][0]
    non_emitting_hidden_states.add(source_state)
    # Ensure nothing conflicts
    if emitting_hidden_states & non_emitting_hidden_states != set():
        raise ValueError('Some states are reportedly non-emitting and emitting at the same time')
    # Build out HMM structure
    transitions = {}
    transitions[source_state] = non_emitting_hidden_states | emitting_hidden_states
    for state in non_emitting_hidden_states | emitting_hidden_states:
        transitions[state] = non_emitting_hidden_states | emitting_hidden_states
    emissions = {}
    for state in emitting_hidden_states:
        emissions[state] = symbols.copy()
    for state in non_emitting_hidden_states:
        emissions[state] = {}
    return transitions, emissions
```