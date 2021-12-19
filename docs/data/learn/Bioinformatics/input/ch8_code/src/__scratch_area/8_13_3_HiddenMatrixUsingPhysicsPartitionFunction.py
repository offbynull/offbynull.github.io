from math import nan, dist, e


def partition_func(
        head_perc,  # data point
        head_bias,  # center
        stiffness
):
    return e ** (-stiffness * dist(head_perc, head_bias))


def estimate_hidden_matrix(
        head_biases: list[float],
        head_percs: list[float],
        stiffness: float):
    hidden_matrix = [[nan] * len(head_percs) for _ in head_biases]
    for j, head_perc in enumerate(head_percs):
        total_pf = sum(partition_func([head_perc], [head_bias], stiffness) for head_bias in head_biases)
        for i, head_bias in enumerate(head_biases):
            pf = partition_func([head_perc], [head_bias], stiffness)
            hidden_matrix[i][j] = pf / total_pf
    return hidden_matrix


if __name__ == '__main__':
    hidden_matrix = estimate_hidden_matrix(
        [-2.5, 2.5],
        [-3, -2, 0, 2, 3],
        1
    )
    print('\n'.join(f'{v}' for v in hidden_matrix))