from math import nan, dist, e

# Exercise Break: Compute HiddenMatrix using the Newtonian inverse-square law for the three centers and eight data
# points shown in the figure below.

# MY ANSWER
# ---------
centers = [
    (3, 9/2),
    (9, 5),
    (6, 3/2)
]

points = [
    (1.0, 6.0),
    (1.0, 3.0),
    (3.0, 4.0),
    (5.0, 6.0),
    (5.0, 2.0),
    (7.0, 1.0),
    (8.0, 7.0),
    (10.0, 3.0)
]


def partition_func(
        head_perc,  # data point
        head_bias,  # center
        stiffness
):
    return e ** (-stiffness * dist(head_perc, head_bias))


def estimate_hidden_matrix(
        head_biases: list[tuple[float, ...]],
        head_percs: list[tuple[float, ...]],
        stiffness: float):
    hidden_matrix = [[nan] * len(head_percs) for _ in head_biases]
    for j, head_perc in enumerate(head_percs):
        total_pf = sum(partition_func(head_perc, head_bias, stiffness) for head_bias in head_biases)
        for i, head_bias in enumerate(head_biases):
            pf = partition_func(head_perc, head_bias, stiffness)
            hidden_matrix[i][j] = pf / total_pf
    return hidden_matrix


if __name__ == '__main__':
    hidden_matrix = estimate_hidden_matrix(
        centers,
        points,
        1
    )
    print('\n'.join(f'membership to {c}={v}' for c, v in zip(centers, hidden_matrix)))