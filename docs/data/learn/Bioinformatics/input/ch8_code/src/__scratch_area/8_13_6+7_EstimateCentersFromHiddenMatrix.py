from math import nan, dist, e


def dot_product(a, b):
    return sum(e_a * e_b for e_a, e_b in zip(a, b))


def estimate_center_coordinate(
        center_idx: int,   # which center is it (row in hidden matrix)
        coord_idx: int,    # which coordinate of center is it (e.g. x or y or ...)
        data_pts: list[tuple[float, ...]],
        hidden_matrix: list[list[float]]
):
    total = sum(hidden_matrix[center_idx])
    bias = dot_product(
        [p[coord_idx] for p in data_pts],
        hidden_matrix[center_idx]
    ) / total
    return bias


def estimate_centers(
        coords: int,
        data_pts: list[tuple[float, ...]],
        hidden_matrix: list[list[float]]
):
    centers = []
    for center_idx, _ in enumerate(hidden_matrix):
        center = []
        for coord_idx in range(coords):
            center.append(estimate_center_coordinate(center_idx, coord_idx, data_pts, hidden_matrix))
        centers.append(tuple(center))
    return centers


if __name__ == '__main__':
    centers = estimate_centers(
        1,
        [(-3,), (-2,), (0,), (2,), (3,)],
        [
            [0.993, 0.983, 0.500, 0.018, 0.007],
            [0.007, 0.018, 0.500, 0.982, 0.993]
        ]
    )
    print(f'{centers=}')