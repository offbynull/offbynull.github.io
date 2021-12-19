from statistics import mean


# conditional probability that you'll get head_perc_in_seq given coin_head_prob -- Pr(head_perc_in_seq|coin_head_prob)
def cond_prob(
        coin_head_bias,
        head_perc_in_seq,
        flips_in_seq):
    coin_tail_prob = 1 - coin_head_bias
    tail_perc_in_seq = 1 - head_perc_in_seq
    return coin_head_bias ** (flips_in_seq * head_perc_in_seq) * coin_tail_prob ** (flips_in_seq * tail_perc_in_seq)


def estimate_hidden_vector(
        a_head_bias: float,
        b_head_bias: float,
        head_perc: list[float],
        flips_per_seq: int
):
    odds_a_in_hidden_vec = [cond_prob(a_head_bias, h, flips_per_seq) for h in head_perc]
    odds_b_in_hidden_vec = [cond_prob(b_head_bias, h, flips_per_seq) for h in head_perc]
    hidden_vector = [1 if a > b else 0 for a, b in zip(odds_a_in_hidden_vec, odds_b_in_hidden_vec)]
    return odds_a_in_hidden_vec, odds_b_in_hidden_vec, hidden_vector


if __name__ == '__main__':
    head_percs = [0.4, 0.9, 0.8, 0.3, 0.7]
    print(f'{estimate_hidden_vector(0.6, 0.82, head_percs, 10)=}')

    # THIS IS ESTIMATING THE HIDDEN VECTOR
    # IN:  header percentages + coin biases
    # OUT: estimated hidden vector
