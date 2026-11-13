from math import nan


def cond_prob(
        coin_head_bias,
        head_perc_in_seq,
        flips_in_seq):
    coin_tail_prob = 1 - coin_head_bias
    tail_perc_in_seq = 1 - head_perc_in_seq
    return coin_head_bias ** (flips_in_seq * head_perc_in_seq) * coin_tail_prob ** (flips_in_seq * tail_perc_in_seq)


# confidence is referred to as responsibility in the book -- how "responsible" is a cluster center for attracting it
def cond_prob_confidence(
        a_head_bias,
        b_head_bias,
        head_perc,
        flips_in_seq):
    a_cp = cond_prob(a_head_bias, head_perc, flips_in_seq)
    b_cp = cond_prob(b_head_bias, head_perc, flips_in_seq)
    a_confidence = a_cp / (a_cp + b_cp)
    b_confidence = b_cp / (a_cp + b_cp)
    return a_confidence, b_confidence


def cond_prob_confidence_profile(
        a_head_bias: float,
        b_head_bias: float,
        head_percs: list[float],
        flips_per_seq: int):
    ret = [[], []]
    for head_perc in head_percs:
        a_conf, b_conf = cond_prob_confidence(a_head_bias, b_head_bias, head_perc, flips_per_seq)
        ret[0].append(a_conf)
        ret[1].append(b_conf)
    return ret


if __name__ == '__main__':
    hidden_matrix = cond_prob_confidence_profile(0.6, 0.82, [0.4, 0.9, 0.8, 0.3, 0.7], 10)
    print('\n'.join(f'{v}' for v in hidden_matrix))


# THIS IS CALLED THE E-STEP. The generic formula (more than 2 head biases) for the responsibility profile is as
# follows. Note that this is generating a "hidden matrix" -- similar to "hidden vector" but it's a "hidden vector" for
# each row the values within are for the thing/coin that generated that head percentage ...
def cond_prob_confidence_profile_generic(
        head_biases: list[float],
        head_percs: list[float],
        flips_per_seq: int):
    hidden_matrix = [[nan] * len(head_percs) for _ in head_biases]
    for j, head_perc in enumerate(head_percs):
        total_cp = sum(cond_prob(head_bias, head_perc, flips_per_seq) for head_bias in head_biases)
        for i, head_bias in enumerate(head_biases):
            cp = cond_prob(head_bias, head_perc, flips_per_seq)
            hidden_matrix[i][j] = cp / total_cp
    return hidden_matrix


if __name__ == '__main__':
    hidden_matrix = cond_prob_confidence_profile_generic(
        [0.6, 0.82],
        [0.4, 0.9, 0.8, 0.3, 0.7],
        10
    )
    print('\n'.join(f'{v}' for v in hidden_matrix))