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
