from math import nan


def dot_product(a, b):
    return sum(e_a * e_b for e_a, e_b in zip(a, b))


# THIS IS CALLED THE M-STEP. Instead of being a hidden vector of 1s and 0s, it's a hidden vector of in-betweens for
# each coin + each data point (hidden matrix AKA responsibility profile)
def confidence_profile_to_biases(
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
    biases = confidence_profile_to_biases(
        [0.4, 0.9, 0.8, 0.3, 0.7],
        [
            [0.97, 0.12, 0.29, 0.99, 0.55],
            [0.03, 0.88, 0.71, 0.01, 0.45]
        ]
    )
    print(f'{biases=}')