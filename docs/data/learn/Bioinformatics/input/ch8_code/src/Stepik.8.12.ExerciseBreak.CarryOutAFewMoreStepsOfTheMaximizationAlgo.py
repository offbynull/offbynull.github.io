import math
import random
from collections import defaultdict
from math import dist, nan
from statistics import mean

# Exercise Break: Carry out a few more steps of the expectation maximization algorithm for the data in the figure on the
# previous step. When should we stop the algorithm?

# MY ANSWER
# ---------
# Probably once the biases stop going down (or the growth is below some threshold)


def cond_prob(
        coin_head_bias,
        head_perc_in_seq,
        flips_in_seq):
    coin_tail_prob = 1 - coin_head_bias
    tail_perc_in_seq = 1 - head_perc_in_seq
    return coin_head_bias ** (flips_in_seq * head_perc_in_seq) * coin_tail_prob ** (flips_in_seq * tail_perc_in_seq)


def e_step(
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


def dot_product(a, b):
    return sum(e_a * e_b for e_a, e_b in zip(a, b))


def m_step(
        head_percs: list[float],
        hidden_matrix: list[list[float]]
):
    biases = []
    for hidden_vector in hidden_matrix:
        total = sum(hidden_vector)
        bias = dot_product(head_percs, hidden_vector) / total
        biases.append(bias)
    return biases


if __name__ == '__main__':
    head_percs = [0.4, 0.9, 0.8, 0.3, 0.7]
    flips_per_seq = 10
    hidden_matrix = [
        [0.97, 0.12, 0.29, 0.99, 0.55],
        [0.03, 0.88, 0.71, 0.01, 0.45]
    ]
    for _ in range(100):
        biases = m_step(head_percs, hidden_matrix)
        hidden_matrix = e_step(biases, head_percs, flips_per_seq)
        print(f'{biases=}')
        print(f'{hidden_matrix=}')
        print(f'----')