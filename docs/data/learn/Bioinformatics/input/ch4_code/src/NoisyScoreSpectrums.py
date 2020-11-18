from bisect import bisect_left
from typing import List, Tuple

from TheoreticalSpectrumOfCyclicPeptide import theoretical_spectrum_of_cyclic_peptide
from Utils import get_amino_acid_to_mass_table, N


def order_spectrums(s1: List[N], s2: List[N]) -> Tuple[List[N], List[N]]:
    if len(s1) < len(s2):
        return s1, s2
    elif len(s1) == len(s2):
        x = sorted([s1, s2])  # tie-breaker
        return x[0], x[1]
    else:
        return s2, s1


def scan_for_unoccupied_slot(arr: List[N], idx: int, unoccupied_const: N) -> int:
    while idx < len(arr) and arr[idx] != unoccupied_const:
        idx += 1
    if idx < len(arr):
        return idx
    idx -= 1
    while idx >= 0 and arr[idx] != unoccupied_const:
        idx -= 1
    if idx >= 0:
        return idx
    raise ValueError('No unoccupied slots')


def spectrum_distance(s1: List[N], s2: List[N]) -> List[N]:
    s_shorter, s_longer = order_spectrums(s1, s2)
    dists = [-1.0] * len(s_longer)
    for ss_idx, ss_mass in enumerate(reversed(s_shorter)):
        sl_idx = bisect_left(s_longer, ss_mass)
        sl_idx = scan_for_unoccupied_slot(dists, sl_idx, -1.0)
        sl_mass = s_longer[sl_idx]
        dist = abs(ss_mass - sl_mass)
        dists[sl_idx] = dist
    return dists


def score_spectrums(s1: List[float], s2: List[float], dist_tolerance=0.0) -> int:
    s_shorter, s_longer = order_spectrums(s1, s2)
    dists = spectrum_distance(s_shorter, s_longer)
    return sum(
        map(
            lambda d: 1,
            filter(
                lambda d: d != -1.0 and d <= dist_tolerance,
                dists
            )
        )
    )







if __name__ == '__main__':
    print(f'{spectrum_distance([0,1,2], [0,0,0,4])}')
    print(f'{spectrum_distance([0,5,6], [0,0,0,4])}')
    print(f'{spectrum_distance([0,1,4], [0,0,0,2])}')
    print(f'{spectrum_distance([0,5,6], [0,5,5,5])}')
    print(f'{spectrum_distance([0,5,6,6], [0,5,5,5])}')
#     x = top_n_peptides_including_last_place_ties(
#         [
#             ['N', 'Q', 'E'],
#             ['N', 'Q', 'A'],
#             ['N', 'Q', 'W']
#         ],
#         theoretical_spectrum_of_cyclic_peptide(['N', 'Q', 'E', 'L']),
#         1,
#         dict([(k, float(v)) for k, v in get_amino_acid_to_mass_table().items()])
#     )
#     print(f'{x}')