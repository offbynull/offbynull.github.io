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
    # exp_spec = [71.1, 97.3, 114.1, 121.9, 125.3, 127.9, 146.8, 147.0, 156.3, 163.2, 165.7, 170.0, 176.3, 178.4, 242.2, 243.8, 257.7, 261.0, 291.3, 294.0, 303.0, 325.9, 333.0, 333.5, 374.3, 377.8, 382.8, 388.7, 390.2, 391.2, 400.2, 403.3, 405.1, 408.2, 409.7, 413.5, 452.5, 461.0, 473.0, 504.0, 504.7, 536.2, 538.0, 546.8, 548.5, 552.0, 552.8, 570.0, 574.9, 588.4, 590.2, 616.9, 618.0, 633.1, 636.1, 650.6, 651.0, 654.9, 657.3, 676.8, 688.2, 698.7, 702.3, 716.8, 721.8, 731.1, 733.2, 738.9, 752.4, 754.7, 754.8, 762.4, 765.2, 770.1, 796.2, 798.2, 860.9, 878.1, 878.2, 878.7, 879.7, 886.1, 894.7, 911.4, 912.5, 924.7, 936.2, 942.8, 945.8, 964.4, 965.8, 978.1, 995.3, 995.5, 1006.6, 1006.9, 1007.7, 1024.8, 1025.0, 1026.8, 1041.9, 1080.3, 1099.1, 1104.3, 1106.0, 1112.9, 1122.0, 1131.0, 1139.9, 1140.7, 1144.5, 1154.9, 1161.7, 1166.7, 1170.0, 1171.8, 1173.1, 1189.0, 1195.4, 1197.8, 1200.7, 1211.6, 1269.2, 1292.3, 1308.4, 1327.3, 1342.7]
    #
    # p = [147.0, 114.0, 128.0, 163.0, 170.0, 76.0, 80.0, 146.0, 97.0, 64.0, 71.0, 76.0]
    # s = score_spectrums(
    #     exp_spec,
    #     theoretical_spectrum_of_cyclic_peptide_with_noisy_aminoacid_masses(p, {aa: aa for aa in p}, 0.6)
    # )
    # print(f'{s}')
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