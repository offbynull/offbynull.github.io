from statistics import mean


def estimate_hidden_vector(
        a_head_bias: float,
        b_head_bias: float,
        head_perc: list[float],
        flips_per_seq: int
):
    heads_per_seq = [round(p * flips_per_seq) for p in head_perc]
    tails_per_seq = [flips_per_seq - h for h in heads_per_seq]
    a_tail_bias = 1 - a_head_bias
    b_tail_bias = 1 - b_head_bias
    odds_a_in_hidden_vec = [a_head_bias ** h * a_tail_bias ** t for h, t in zip(heads_per_seq, tails_per_seq)]
    odds_b_in_hidden_vec = [b_head_bias ** h * b_tail_bias ** t for h, t in zip(heads_per_seq, tails_per_seq)]
    hidden_vector = [1 if a > b else 0 for a, b in zip(odds_a_in_hidden_vec, odds_b_in_hidden_vec)]
    return odds_a_in_hidden_vec, odds_b_in_hidden_vec, hidden_vector


if __name__ == '__main__':
    head_percs = [0.4, 0.9, 0.8, 0.3, 0.7]
    print(f'{estimate_hidden_vector(0.6, 0.82, head_percs, 10)=}')

    # THIS IS ESTIMATING THE HIDDEN VECTOR
    # IN:  header percentages + coin biases
    # OUT: estimated hidden vector
