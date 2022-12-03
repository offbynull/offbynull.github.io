from sys import stdin


def optimal_value(capacity, weights, values):
    value = 0.
    values_per_lbs = sorted((v / w, w) for w, v in zip(weights, values))
    while capacity > 0 and values_per_lbs:
        value_per_lbs, total_lbs = values_per_lbs.pop()
        extraction_amount = min(capacity, total_lbs)
        value += extraction_amount * value_per_lbs
        capacity -= extraction_amount
    return value


if __name__ == "__main__":
    data = list(map(int, stdin.read().split()))
    n, capacity = data[0:2]
    values = data[2:(2 * n + 2):2]
    weights = data[3:(2 * n + 2):2]
    opt_value = optimal_value(capacity, weights, values)
    print("{:.10f}".format(opt_value))
