from statistics import mean


def dot_product(a, b):
    return sum(e_a * e_b for e_a, e_b in zip(a, b))


def sub_scalar(vector, scalar):
    return [x - scalar for x in vector]


def sub_vector(v1, v2):
    return [x - y for x, y in zip(v1, v2)]


def estimate_coin_head_bias(
        hidden_vector: list[int],
        head_perc: list[float],
):
    all_ones_vector = [1 for _ in hidden_vector]
    a_percs = dot_product(hidden_vector, head_perc) / sum(hidden_vector)
    b_percs = dot_product(sub_vector(hidden_vector, all_ones_vector), head_perc)\
              / sum(sub_vector(hidden_vector, all_ones_vector))
    return a_percs, b_percs


if __name__ == '__main__':
    head_percs = [0.4, 0.9, 0.8, 0.3, 0.7]
    hidden_vector = [1, 0, 0, 1, 0]
    print(f'{estimate_coin_head_bias(hidden_vector, head_percs)=}')

    # THIS IS ESTIMATING THE COIN BIASES
    # IN:  header percentages + coin used per flip sequence AS VECTOR (A or B)
    # OUT: estimated coin bias (A and B)
