from itertools import product

from helpers.Utils import slide_window

# Exercise Break: Compute Pr(x, π) for the x and π in the reproduced figure below. Can you find a better explanation for
# x = “THTHHHTHTTH” than π = FFFBBBBBFFF?
#
# State transitions:
# F->F=0.9, B->B=0.9, F->B=0.1, B->F=0.1
#
# Emissions:
# F->H=0.5,  F->T=0.5
# B->H=0.75, B->T=0.25
#
# Pr(x, π) = Pr(x|π) · Pr(π)


# MY ANSWER
# ---------
# Pr(π) = 0.5 * multiply(for x in slide_window(FFFBBBBBFFF, 2)) = 0.002152336050000001
# Pr(x|π) = multiply(Pr(a,b) for a, b in zip(FFFBBBBBFFF, THTHHHTHTTH)) = 0.0012359619140625
# Pr(x, π) = Pr(x|π) · Pr(π)
expected = 0.0012359619140625 * 0.002152336050000001
#
# The following π produces a better result for x = THTHHHTHTTH
hidden_states = {'F', 'B'}
hidden_state_transition_probs = {('F', 'F'): 0.9, ('B', 'B'): 0.9, ('F', 'B'): 0.1, ('B', 'F'): 0.1}
symbols = {'T', 'H'}
state_symbol_emission_probs = {('F', 'H'): 0.5, ('F', 'T'): 0.5, ('B', 'H'): 0.75, ('B', 'T'): 0.25}
emitted_symbols = 'THTHHHTHTTH'
for hidden_state_seq in product(list(hidden_states), repeat=11):
    hidden_state_seq = ''.join(hidden_state_seq)
    hidden_state_prob = 1.0 / len(hidden_states)
    for (s1, s2), _ in slide_window(hidden_state_seq, 2):
        hidden_state_prob *= hidden_state_transition_probs[s1, s2]
    state_emission_prob = 1.0
    for hs, es in zip(hidden_state_seq, emitted_symbols):
        state_emission_prob *= state_symbol_emission_probs[hs, es]
    actual = hidden_state_prob * state_emission_prob
    if actual > expected:
        print(f'{state_emission_prob=}')
        print(f'{hidden_state_prob=}')
        print(f'{hidden_state_seq=}')
        print(f'{actual=} vs {expected=}')
        print('----')
