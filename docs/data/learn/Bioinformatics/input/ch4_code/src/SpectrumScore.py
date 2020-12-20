from bisect import bisect_left
from typing import List, Tuple, Optional

from PeptideType import PeptideType
from TheoreticalSpectrumTolerances import theoretical_spectrum_tolerances
from TheoreticalSpectrum_PrefixSum import theoretical_spectrum


# MARKDOWN
def scan_left(
        exp_spec: List[float],
        exp_spec_lo_idx: int,
        exp_spec_start_idx: int,
        theo_mid_mass: float,
        theo_min_mass: float
) -> Optional[int]:
    found_dist = None
    found_idx = None
    for idx in range(exp_spec_start_idx, exp_spec_lo_idx - 1, -1):
        exp_mass = exp_spec[idx]
        if exp_mass < theo_min_mass:
            break
        dist_to_theo_mid_mass = abs(exp_mass - theo_mid_mass)
        if found_dist is None or dist_to_theo_mid_mass < found_dist:
            found_idx = idx
            found_dist = dist_to_theo_mid_mass
    return found_idx


def scan_right(
        exp_spec: List[float],
        exp_spec_hi_idx: int,
        exp_spec_start_idx: int,
        theo_mid_mass: float,
        theo_max_mass: float
) -> Optional[int]:
    found_dist = None
    found_idx = None
    for idx in range(exp_spec_start_idx, exp_spec_hi_idx):
        exp_mass = exp_spec[idx]
        if exp_mass > theo_max_mass:
            break
        dist_to_theo_mid_mass = abs(exp_mass - theo_mid_mass)
        if found_dist is None or dist_to_theo_mid_mass < found_dist:
            found_idx = idx
            found_dist = dist_to_theo_mid_mass
    return found_idx


def find_closest_within_tolerance(
        exp_spec: List[float],
        exp_spec_lo_idx: int,
        exp_spec_hi_idx: int,
        theo_exact_mass: float,
        theo_min_mass: float,
        theo_max_mass: float
) -> Optional[int]:
    # Binary search exp_spec for the where theo_mid_mass would be inserted (left-most index chosen if already there).
    start_idx = bisect_left(exp_spec, theo_exact_mass, lo=exp_spec_lo_idx, hi=exp_spec_hi_idx)
    if start_idx == exp_spec_hi_idx:
        start_idx -= 1
    # From start_idx - 1, walk left to find the closest possible value to theo_mid_mass
    left_idx = scan_left(exp_spec, exp_spec_lo_idx, start_idx - 1, theo_exact_mass, theo_min_mass)
    # From start_idx, walk right to find the closest possible value to theo_mid_mass
    right_idx = scan_right(exp_spec, exp_spec_hi_idx, start_idx, theo_exact_mass, theo_max_mass)
    if left_idx is None and right_idx is None:  # If nothing found, return None
        return None
    if left_idx is None:  # If found something while walking left but not while walking right, return left
        return right_idx
    if right_idx is None:  # If found something while walking right but not while walking left, return right
        return left_idx
    # Otherwise, compare left and right to see which is close to theo_mid_mass and return that
    left_exp_mass = exp_spec[left_idx]
    left_dist_to_theo_mid_mass = abs(left_exp_mass - theo_exact_mass)
    right_exp_mass = exp_spec[left_idx]
    right_dist_to_theo_mid_mass = abs(right_exp_mass - theo_exact_mass)
    if left_dist_to_theo_mid_mass < right_dist_to_theo_mid_mass:
        return left_idx
    else:
        return right_idx


def score_spectrums(
        exp_spec: List[float],  # must be sorted asc
        theo_spec_with_tolerances: List[Tuple[float, float, float]]  # must be sorted asc, items are (expected,min,max)
) -> Tuple[int, float, float]:
    dist_score = 0.0
    within_score = 0
    exp_spec_lo_idx = 0
    exp_spec_hi_idx = len(exp_spec)
    for theo_mass in theo_spec_with_tolerances:
        # Find closest exp_spec mass for theo_mass
        theo_exact_mass, theo_min_mass, theo_max_mass = theo_mass
        exp_idx = find_closest_within_tolerance(
            exp_spec,
            exp_spec_lo_idx,
            exp_spec_hi_idx,
            theo_exact_mass,
            theo_min_mass,
            theo_max_mass
        )
        if exp_idx is None:
            continue
        # Calculate how far the found mass is from the ideal mass (theo_exact_mass) -- a perfect match will add 1.0 to
        # score, the farther out it is away the less gets added to score (min added will be 0.5).
        exp_mass = exp_spec[exp_idx]
        dist = abs(exp_mass - theo_exact_mass)
        max_dist = theo_max_mass - theo_min_mass
        if max_dist > 0.0:
            closeness = 1.0 - (dist / max_dist)
        else:
            closeness = 1.0
        dist_score += closeness
        # Increment within_score for each match. The above block increases dist_score as the found mass gets closer to
        # theo_exact_mass. There may be a case where a peptide with 6 of 10 AAs matches exactly (6 * 1.0) while another
        # peptide with 10 of 10 AAs matching very loosely (10 * 0.5) -- the first peptide will incorrectly win out if
        # only dist_score were used.
        within_score += 1
        # Move up the lower bound for what to consider in exp_spec such that it it's after the exp_spec mass found
        # in this cycle. That is, the next cycle won't consider anything lower than the mass that was found here. This
        # is done because theo_spec may contain multiple copies of the same mass, but a real experimental spectrum won't
        # do that (e.g. a peptide containing 57 twice will have two entries for 57 in its theoretical spectrum, but a
        # real experimental spectrum for that same peptide will only contain 57 -- anything with mass of 57 will be
        # collected into the same bin).
        exp_spec_lo_idx = exp_idx + 1
        if exp_spec_lo_idx == exp_spec_hi_idx:
            break
    return within_score, dist_score, 0.0 if within_score == 0 else dist_score / within_score
# MARKDOWN


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        exp_spec = [float(m) for m in input().strip().split()]
        exp_spec.sort()
        theo_peptide = input().strip()
        theo_type = input().strip()
        theo_mass_table = {e.strip().split(':')[0]: float(e.strip().split(':')[1]) for e in input().strip().split(',')}
        aa_tolerance = float(input().strip())
        theo_spec = theoretical_spectrum(
            list(theo_peptide),
            {'cyclic': PeptideType.CYCLIC, 'linear': PeptideType.LINEAR}[theo_type],
            theo_mass_table
        )
        theo_spec_tols = theoretical_spectrum_tolerances(
            len(theo_peptide),
            {'cyclic': PeptideType.CYCLIC, 'linear': PeptideType.LINEAR}[theo_type],
            aa_tolerance
        )
        score = score_spectrums(exp_spec, [(m, m-t, m+t) for m, t in zip(theo_spec, theo_spec_tols)])
        print(f'The spectrum score for...', end="\n\n")
        print(f'{exp_spec}', end="\n\n")
        print(f'... vs ...', end="\n\n")
        print(f'{theo_spec}', end="\n\n")
        print(f'... with {aa_tolerance} amino acid tolerance is...', end="\n\n")
        print(f'{score}', end="\n\n")
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()


# if __name__ == '__main__':
#     # x = theoretical_spectrum_of_cyclic_peptide_with_noisy_aminoacid_masses([1, 2, 3], {1: 1, 2: 2, 3: 3}, 0.1)
#     # print(f'{x}')
#     # x = theoretical_spectrum_of_cyclic_peptide([1, 2, 3], {1: 1, 2: 2, 3: 3})
#     # print(f'{x}')
#     # x = theoretical_spectrum_of_linear_peptide_with_noisy_aminoacid_masses([1, 2, 3], {1: 1, 2: 2, 3: 3}, 0.1)
#     # print(f'{x}')
#     # x = theoretical_spectrum_of_linear_peptide([1, 2, 3], {1: 1, 2: 2, 3: 3})
#     # print(f'{x}')
#     exp_spec = [370.5, 374.4, 389.4, 391.2, 408.0, 419.2, 426.2, 442.3, 445.4, 460.3, 470.4, 476.4, 490.3, 504.3, 505.4, 518.2, 535.1, 545.5, 552.3, 561.3, 587.2, 599.3, 615.2, 616.4, 617.3, 632.4, 633.4, 635.2, 650.5, 651.4, 701.5, 702.4, 711.5, 717.3, 720.0, 729.3, 748.4, 761.6, 762.4, 763.4, 778.6, 779.4, 780.4, 781.4, 796.3, 861.4, 875.4, 876.4, 877.6, 878.4, 892.4, 893.4, 894.4, 895.5, 926.4, 943.4, 974.5, 975.5, 976.4, 978.4, 1004.5, 1006.5, 1021.5, 1022.7, 1023.5, 1038.5, 1039.3, 1041.5, 1042.4, 1056.5, 1118.6, 1119.6, 1136.6, 1137.6, 1138.5, 1155.5, 1156.6, 1167.6, 1170.6, 1184.4, 1219.6, 1221.5, 1222.6, 1238.6, 1239.6, 1249.5, 1255.5, 1265.5, 1266.5, 1267.6]
#     # exp_spec = [371.5, 375.4, 390.4, 392.2, 409.0, 420.2, 427.2, 443.3, 446.4, 461.3, 471.4, 477.4, 491.3, 505.3, 506.4, 519.2, 536.1, 546.5, 553.3, 562.3, 588.2, 600.3, 616.2, 617.4, 618.3, 633.4, 634.4, 636.2, 651.5, 652.4, 702.5, 703.4, 712.5, 718.3, 721.0, 730.3, 749.4, 762.6, 763.4, 764.4, 779.6, 780.4, 781.4, 782.4, 797.3, 862.4, 876.4, 877.4, 878.6, 879.4, 893.4, 894.4, 895.4, 896.5, 927.4, 944.4, 975.5, 976.5, 977.4, 979.4, 1005.5, 1007.5, 1022.5, 1023.7, 1024.5, 1039.5, 1040.3, 1042.5, 1043.4, 1057.5, 1119.6, 1120.6, 1137.6, 1138.6, 1139.5, 1156.5, 1157.6, 1168.6, 1171.6, 1185.4, 1220.6, 1222.5, 1223.6, 1239.6, 1240.6, 1250.5, 1256.5, 1266.5, 1267.5, 1268.6]
#
#     p = [99.0, 128.0, 113.0, 147.0, 97.0, 147.0, 147.0, 114.0, 128.0, 163.0]
#     for j in range(0, len(p) + 1):
#         print(f'{j}')
#         for sp, _ in slide_window(p, j, cyclic=True):
#             theo_spec = theoretical_spectrum_of_cyclic_peptide_with_noisy_aminoacid_masses(sp, {aa: aa for aa in sp}, 0.6)
#             s = score_spectrums(exp_spec, theo_spec)
#             print(f'{sp} = {s}  --  {s[0]} of {len(theo_spec)} matched ({s[0] / len(theo_spec)})')
#     s = score_spectrums(
#         exp_spec,
#         theoretical_spectrum_of_cyclic_peptide_with_noisy_aminoacid_masses(p, {aa: aa for aa in p}, 0.6)
#     )
#     print(f'{s}')
#     # p = [163.0, 128.0, 114.0, 147.0, 147.0, 97.0, 82.0, 166.0, 145.0]
#     # s = score_spectrums(
#     #     exp_spec,
#     #     theoretical_spectrum_of_cyclic_peptide_with_noisy_aminoacid_masses(p, {aa: aa for aa in p}, 0.6)
#     # )
#     # print(f'{s}')
#     # p = [147, 97, 147, 147, 114, 128, 163, 99, 71, 156]
#     # s = score_spectrums(
#     #     exp_spec,
#     #     theoretical_spectrum_of_cyclic_peptide_with_noisy_aminoacid_masses(p, {aa: aa for aa in p}, 0.6)
#     # )
#     # print(f'{s}')
#     pass