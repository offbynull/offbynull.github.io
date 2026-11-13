from math import nan, dist, e

# Exercise Break: Compute HiddenMatrix using the Newtonian inverse-square law for the three centers and eight data
# points shown in the figure below.

# MY ANSWER
# ---------
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

hidden_matrix = [  # output of  previous exercise break (compute hidden matrix)
    [0.9818948854853473, 0.9354016117872895, 0.9643528577158651, 0.7584084916516269, 0.10871554115402421, 0.014324115311329383, 0.03290635848683629, 0.006396709467670041],
    [0.0037705712420412064, 0.002988479462717017, 0.003628047890133547, 0.14962265961104068, 0.017998652167730902, 0.03327749869389019, 0.9417763937162321, 0.87886057434317],
    [0.014334543272611466, 0.06160990874999347, 0.03201909439400137, 0.0919688487373323, 0.8732858066782448, 0.9523983859947803, 0.02531724779693167, 0.11474271618915992]
]


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


# if __name__ == '__main__':
#     centers = estimate_centers(
#         1,
#         [(-3,), (-2,), (0,), (2,), (3,)],
#         [
#             [0.993, 0.983, 0.500, 0.018, 0.007],
#             [0.007, 0.018, 0.500, 0.982, 0.993]
#         ]
#     )
#     print(f'{centers=}')


if __name__ == '__main__':
    centers = estimate_centers(
        2,
        points,
        hidden_matrix
    )
    print(f'{centers=}')