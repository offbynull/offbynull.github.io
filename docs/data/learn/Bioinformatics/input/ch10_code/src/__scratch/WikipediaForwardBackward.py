states = ('A', 'B')
end_state = 'E'

emissions = ('x', 'y')

start_probabilities = {'A': 0.5, 'B': 0.5}

transition_probabilities = {
    'A': {'A': 0.9, 'B': 0.1, 'E': 1.0},
    'B': {'A': 0.2, 'B': 0.8, 'E': 1.0},
}

emission_probabilities = {
    'A': {'x': 0.3, 'y': 0.7},
    'B': {'x': 0.1, 'y': 0.9},
}


def fwd_bkw(emissions, states, start_prob, trans_prob, emm_prob, end_st):
    """Forward–backward algorithm."""
    # Forward part of the algorithm
    fwd = []
    for i, symbol in enumerate(emissions):
        f_curr = {}
        for from_state in states:
            if i == 0:
                # base case for the forward part
                prev_f_sum = start_prob[from_state]
            else:
                prev_f_sum = sum(f_prev[to_state] * trans_prob[to_state][from_state] for to_state in states)

            f_curr[from_state] = emm_prob[from_state][symbol] * prev_f_sum

        fwd.append(f_curr)
        f_prev = f_curr

    p_fwd = sum(f_curr[k] * trans_prob[k][end_st] for k in states)

    # Backward part of the algorithm
    bkw = []
    for i, symbol in enumerate(reversed(emissions[1:] + (None,))):
        b_curr = {}
        for from_state in states:
            if i == 0:
                # base case for backward part
                b_curr[from_state] = trans_prob[from_state][end_st]
            else:
                b_curr[from_state] = 0.0
                for to_state in states:
                    b_curr[from_state] += trans_prob[from_state][to_state] * emm_prob[to_state][symbol] * b_prev[to_state]

        bkw.insert(0,b_curr)
        b_prev = b_curr

    p_bkw = sum(start_prob[l] * emm_prob[l][emissions[0]] * b_curr[l] for l in states)

    # Merging the two parts
    posterior = []
    for i in range(len(emissions)):
        posterior.append({st: fwd[i][st] * bkw[i][st] / p_fwd for st in states})

    assert p_fwd == p_bkw
    return fwd, bkw, posterior


def example():
    return fwd_bkw(emissions,
                   states,
                   start_probabilities,
                   transition_probabilities,
                   emission_probabilities,
                   end_state)


for line in example():
    print(*line)