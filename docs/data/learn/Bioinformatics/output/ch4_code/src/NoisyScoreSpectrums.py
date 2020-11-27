import enum
from bisect import bisect_left
from enum import Enum
from typing import List, Tuple, Dict, Optional

from TheoreticalSpectrumOfCyclicPeptide import theoretical_spectrum_of_cyclic_peptide
from TheoreticalSpectrumOfLinearPeptide import theoretical_spectrum_of_linear_peptide
from Utils import T, slide_window


def determine_mass_tolerance(
        p: List[T],
        mass_table: Dict[T, float],
        amino_acid_mass_tolerance: float
) -> Tuple[float, float, float]:
    p_mass_tolerance = len(p) * amino_acid_mass_tolerance
    p_mass = sum([mass_table[aa] for aa in p])
    min_p_mass = p_mass - p_mass_tolerance
    max_p_mass = p_mass + p_mass_tolerance
    return p_mass, min_p_mass, max_p_mass


def theoretical_spectrum_of_cyclic_peptide_with_noisy_aminoacid_masses(
        peptide: List[T],
        mass_table: Dict[T, float],
        amino_acid_mass_tolerance: float
) -> List[Tuple[float, float, float]]:
    # Add 0 mass
    ret = [(0.0, 0.0, 0.0)]
    # Add masses for sub-peptides
    for k in range(1, len(peptide)):
        for subpeptide, _ in slide_window(peptide, k, cyclic=True):
            subpeptide_tolerance = determine_mass_tolerance(subpeptide, mass_table, amino_acid_mass_tolerance)
            ret.append(subpeptide_tolerance)
    # Add mass for full peptide
    peptide_tolerance = determine_mass_tolerance(peptide, mass_table, amino_acid_mass_tolerance)
    ret.append(peptide_tolerance)
    # Sort and return
    ret.sort(key=lambda x: x[0])
    return ret


def theoretical_spectrum_of_linear_peptide_with_noisy_aminoacid_masses(
        peptide: List[T],
        mass_table: Dict[T, float],
        amino_acid_mass_tolerance: float
) -> List[Tuple[float, float, float]]:
    # Add 0 mass
    ret = [(0.0, 0.0, 0.0)]
    # Add masses for sub-peptides
    for k in range(1, len(peptide) + 1):
        for subpeptide, _ in slide_window(peptide, k):
            subpeptide_tolerance = determine_mass_tolerance(subpeptide, mass_table, amino_acid_mass_tolerance)
            ret.append(subpeptide_tolerance)
    # Sort and return
    ret.sort(key=lambda x: x[0])
    return ret


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
        theo_mid_mass: float,
        theo_min_mass: float,
        theo_max_mass: float
) -> Optional[int]:
    # Binary search exp_spec for the where theo_mid_mass would be inserted (left-most index chosen if already there).
    start_idx = bisect_left(exp_spec, theo_mid_mass, lo=exp_spec_lo_idx, hi=exp_spec_hi_idx)
    if start_idx == exp_spec_hi_idx:
        start_idx -= 1
    # From start_idx - 1, walk left to find the closest possible value to theo_mid_mass
    left_idx = scan_left(exp_spec, exp_spec_lo_idx, start_idx - 1, theo_mid_mass, theo_min_mass)
    # From start_idx, walk right to find the closest possible value to theo_mid_mass
    right_idx = scan_right(exp_spec, exp_spec_hi_idx, start_idx, theo_mid_mass, theo_max_mass)
    if left_idx is None and right_idx is None:  # If nothing found, return None
        return None
    if left_idx is None:  # If found something while walking left but not while walking right, return left
        return right_idx
    if right_idx is None:  # If found something while walking right but not while walking left, return right
        return left_idx
    # Otherwise, compare left and right to see which is close to theo_mid_mass and return that
    left_exp_mass = exp_spec[left_idx]
    left_dist_to_theo_mid_mass = abs(left_exp_mass - theo_mid_mass)
    right_exp_mass = exp_spec[left_idx]
    right_dist_to_theo_mid_mass = abs(right_exp_mass - theo_mid_mass)
    if left_dist_to_theo_mid_mass < right_dist_to_theo_mid_mass:
        return left_idx
    else:
        return right_idx


def score_spectrums(
        exp_spec: List[float],
        theo_spec_with_tolerances: List[Tuple[float, float, float]]
) -> Tuple[int, float, float]:
    dist_score = 0.0
    within_score = 0
    exp_spec_lo_idx = 0
    exp_spec_hi_idx = len(exp_spec)
    for theo_mass in theo_spec_with_tolerances:
        # Find closest exp_spec mass for theo_mass
        theo_mid_mass, theo_min_mass, theo_max_mass = theo_mass
        exp_idx = find_closest_within_tolerance(
            exp_spec,
            exp_spec_lo_idx,
            exp_spec_hi_idx,
            theo_mid_mass,
            theo_min_mass,
            theo_max_mass
        )
        if exp_idx is None:
            continue
        # Calculate how far the found mass is from the ideal mass (theo_mid_mass) -- a perfect match will add 1.0 to
        # score, the farther out it is away the less gets added to score (min added will be 0.5).
        exp_mass = exp_spec[exp_idx]
        dist = abs(exp_mass - theo_mid_mass)
        max_dist = theo_max_mass - theo_min_mass
        if max_dist > 0.0:
            closeness = 1.0 - (dist / max_dist)
        else:
            closeness = 1.0
        dist_score += closeness
        # Add 1 for each match. Why? because the above block increases the score to 1.0 as the spectrum mass gets
        # closer. There may be a case where a peptide with 6 of 10 AAs matches exactly (6 * 1.0) while another peptide
        # with 10 of 10 AAs matching very loosely (10 * 0.5) -- the first peptide will incorrectly win out if only
        # dist_score were used.
        within_score += 1
        # Move up the lower bound for what to consider in exp_mass such that it it's after the exp_mass that was found
        # in this cycle. That is, the next cycle won't consider anything lower than the mass that was found here. This
        # is done because theo_spec may contain multiple copies of the same mass, but a real experimental spectrum won't
        # do that (e.g. a peptide containing 57 twice will have two entries for 57 in its theoretical spectrum, but a
        # real experimental spectrum for that same peptide will only contain 57 -- anything with mass of 57 will be
        # collected into the same bin.
        exp_spec_lo_idx = exp_idx + 1
        if exp_spec_lo_idx == exp_spec_hi_idx:
            break
    return (within_score, dist_score, 0.0 if within_score == 0 else dist_score / within_score)


if __name__ == '__main__':
    # x = theoretical_spectrum_of_cyclic_peptide_with_noisy_aminoacid_masses([1, 2, 3], {1: 1, 2: 2, 3: 3}, 0.1)
    # print(f'{x}')
    # x = theoretical_spectrum_of_cyclic_peptide([1, 2, 3], {1: 1, 2: 2, 3: 3})
    # print(f'{x}')
    # x = theoretical_spectrum_of_linear_peptide_with_noisy_aminoacid_masses([1, 2, 3], {1: 1, 2: 2, 3: 3}, 0.1)
    # print(f'{x}')
    # x = theoretical_spectrum_of_linear_peptide([1, 2, 3], {1: 1, 2: 2, 3: 3})
    # print(f'{x}')
    exp_spec = [370.5, 374.4, 389.4, 391.2, 408.0, 419.2, 426.2, 442.3, 445.4, 460.3, 470.4, 476.4, 490.3, 504.3, 505.4, 518.2, 535.1, 545.5, 552.3, 561.3, 587.2, 599.3, 615.2, 616.4, 617.3, 632.4, 633.4, 635.2, 650.5, 651.4, 701.5, 702.4, 711.5, 717.3, 720.0, 729.3, 748.4, 761.6, 762.4, 763.4, 778.6, 779.4, 780.4, 781.4, 796.3, 861.4, 875.4, 876.4, 877.6, 878.4, 892.4, 893.4, 894.4, 895.5, 926.4, 943.4, 974.5, 975.5, 976.4, 978.4, 1004.5, 1006.5, 1021.5, 1022.7, 1023.5, 1038.5, 1039.3, 1041.5, 1042.4, 1056.5, 1118.6, 1119.6, 1136.6, 1137.6, 1138.5, 1155.5, 1156.6, 1167.6, 1170.6, 1184.4, 1219.6, 1221.5, 1222.6, 1238.6, 1239.6, 1249.5, 1255.5, 1265.5, 1266.5, 1267.6]
    # exp_spec = [371.5, 375.4, 390.4, 392.2, 409.0, 420.2, 427.2, 443.3, 446.4, 461.3, 471.4, 477.4, 491.3, 505.3, 506.4, 519.2, 536.1, 546.5, 553.3, 562.3, 588.2, 600.3, 616.2, 617.4, 618.3, 633.4, 634.4, 636.2, 651.5, 652.4, 702.5, 703.4, 712.5, 718.3, 721.0, 730.3, 749.4, 762.6, 763.4, 764.4, 779.6, 780.4, 781.4, 782.4, 797.3, 862.4, 876.4, 877.4, 878.6, 879.4, 893.4, 894.4, 895.4, 896.5, 927.4, 944.4, 975.5, 976.5, 977.4, 979.4, 1005.5, 1007.5, 1022.5, 1023.7, 1024.5, 1039.5, 1040.3, 1042.5, 1043.4, 1057.5, 1119.6, 1120.6, 1137.6, 1138.6, 1139.5, 1156.5, 1157.6, 1168.6, 1171.6, 1185.4, 1220.6, 1222.5, 1223.6, 1239.6, 1240.6, 1250.5, 1256.5, 1266.5, 1267.5, 1268.6]

    p = [99.0, 128.0, 113.0, 147.0, 97.0, 147.0, 147.0, 114.0, 128.0, 163.0]
    for j in range(0, len(p) + 1):
        for sp, _ in slide_window(p, j):
            s = score_spectrums(
                exp_spec,
                theoretical_spectrum_of_cyclic_peptide_with_noisy_aminoacid_masses(sp, {aa: aa for aa in sp}, 0.6)
            )
            print(f'{sp} = {s}')
    s = score_spectrums(
        exp_spec,
        theoretical_spectrum_of_cyclic_peptide_with_noisy_aminoacid_masses(p, {aa: aa for aa in p}, 0.6)
    )
    print(f'{s}')
    # p = [163.0, 128.0, 114.0, 147.0, 147.0, 97.0, 82.0, 166.0, 145.0]
    # s = score_spectrums(
    #     exp_spec,
    #     theoretical_spectrum_of_cyclic_peptide_with_noisy_aminoacid_masses(p, {aa: aa for aa in p}, 0.6)
    # )
    # print(f'{s}')
    # p = [147, 97, 147, 147, 114, 128, 163, 99, 71, 156]
    # s = score_spectrums(
    #     exp_spec,
    #     theoretical_spectrum_of_cyclic_peptide_with_noisy_aminoacid_masses(p, {aa: aa for aa in p}, 0.6)
    # )
    # print(f'{s}')
    pass