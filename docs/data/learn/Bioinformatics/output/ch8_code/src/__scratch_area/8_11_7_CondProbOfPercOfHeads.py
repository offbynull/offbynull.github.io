import math


# Define the conditional probability of generating Data given HiddenVector and Parameters as
#
#                                  n
# Pr(Data|HiddenVector, θA, θB) = ∏   Pr(Data[i]|HiddenVector, Parameters).
#                                  i=1
#
# ... where ...
#
# Pr(Data[i]|HiddenVector, θA, θB) = Pr(Data[i]∣θA) if HiddenVector[i]==1 else Pr(Data[i]∣θB)


# WHAT'S THE POINT? The point is to find the "given" variables that produce Data...
#
#                                     n
#    Pr(Data|HiddenVector, θA, θB) = ∏   Pr(Data[i]|HiddenVector, Parameters).
#        ^          ^      ^   ^      i=1
#        |          |      |   |
#        |          '------+---'
#        |                 |
#    HAVE THIS        FIND THESE


# Pr(Data∣θ)
def cond_prob(
        coin_head_bias,
        head_perc_in_seq,
        flips_in_seq):
    coin_tail_prob = 1 - coin_head_bias
    tail_perc_in_seq = 1 - head_perc_in_seq
    return coin_head_bias ** (flips_in_seq * head_perc_in_seq) * coin_tail_prob ** (flips_in_seq * tail_perc_in_seq)


# Pr(Data[i]|HiddenVector, θA, θB) = Pr(Data[i]∣θA) if HiddenVector[i]==1 else Pr(Data[i]∣θB)
def cond_prob_on_data_elem(
        a_head_bias,
        b_head_bias,
        hidden_vector,
        head_percs,
        flips_in_seq,
        idx):
    if hidden_vector[idx] == 1:
        return cond_prob(a_head_bias, head_percs[idx], flips_in_seq)
    elif hidden_vector[idx] == 0:
        return cond_prob(b_head_bias, head_percs[idx], flips_in_seq)


#                                  n
# Pr(Data|HiddenVector, θA, θB) = ∏   Pr(Data[i]|HiddenVector, Parameters).
#                                  i=1
def cond_prob_on_data(
        a_head_bias,
        b_head_bias,
        hidden_vector,
        head_percs,
        flips_in_seq):
    res = 1
    for i in range(head_percs):
        res *= cond_prob_on_data_elem(a_head_bias, b_head_bias, hidden_vector, head_percs, flips_in_seq, i)
    return res


# GIVEN head_percs, WE'RE TRYING TO FIND VALUES FOR a_head_bias, b_head_bias, AND hidden_vector TO MAXIMIZE THE RESULT
# OF THE cond_prob_on_data() FUNCTION.
#
# cond_prob(?, ?, ?, head_percs, flips_in_seq)  <-- find the correct values for ? to generate the max possible result

