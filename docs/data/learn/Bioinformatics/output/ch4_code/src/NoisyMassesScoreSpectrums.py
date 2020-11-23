from bisect import bisect_left
from typing import List, Tuple, Dict, Optional

from TheoreticalSpectrumOfCyclicPeptide import theoretical_spectrum_of_cyclic_peptide
from Utils import T, slide_window, get_unique_amino_acid_masses_as_dict


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
            subpeptide_mass_tolerance = len(subpeptide) * amino_acid_mass_tolerance
            subpeptide_mass = sum([mass_table[aa] for aa in subpeptide])
            min_subpeptide_mass = subpeptide_mass - subpeptide_mass_tolerance
            max_subpeptide_mass = subpeptide_mass + subpeptide_mass_tolerance
            ret.append((subpeptide_mass, min_subpeptide_mass, max_subpeptide_mass))
    # Add mass for full peptide
    peptide_mass_tolerance = len(peptide) * amino_acid_mass_tolerance
    peptide_mass = sum([mass_table[aa] for aa in peptide])
    min_peptide_mass = peptide_mass - peptide_mass_tolerance
    max_peptide_mass = peptide_mass + peptide_mass_tolerance
    ret.append((peptide_mass, min_peptide_mass, max_peptide_mass))
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
) -> float:
    score = 0
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
        score += closeness
        # Move up the lower bound for what to consider in exp_mass such that it it's after the exp_mass that was found
        # in this cycle. That is, the next cycle won't consider anything lower than the mass that was found here. This
        # is done because theo_spec may contain multiple copies of the same mass, but a real experimental spectrum won't
        # do that (e.g. a peptide containing 57 twice will have two entries for 57 in its theoretical spectrum, but a
        # real experimental spectrum for that same peptide will only contain 57 -- anything with mass of 57 will be
        # collected into the same bin.
        exp_spec_lo_idx = exp_idx + 1
        if exp_spec_lo_idx == exp_spec_hi_idx:
            break
    return score


if __name__ == '__main__':
    for x,y in zip(theoretical_spectrum_of_cyclic_peptide([147, 97, 57, 163, 114], get_unique_amino_acid_masses_as_dict()), theoretical_spectrum_of_cyclic_peptide_with_noisy_aminoacid_masses([147, 97, 57, 163, 114], get_unique_amino_acid_masses_as_dict(), 0.6)):
        print(f'{x} = {y}')
    s = score_spectrums(
        [0.1, 56.8, 153.9, 162.7, 172.0, 220.1, 260.7, 277.2, 301.1, 317.3, 334.1, 340.2, 349.7, 358.0, 363.5, 380.5, 402.8, 415.2, 424.3, 426.6, 427.8, 431.0, 456.4, 472.9, 480.9, 521.1, 563.4, 578.2, 597.8],
        theoretical_spectrum_of_cyclic_peptide_with_noisy_aminoacid_masses([147, 97, 57, 163, 114], get_unique_amino_acid_masses_as_dict(), 0.6)
    )
    print(f'{s}')
    s = score_spectrums(
        [0.1, 56.8, 153.9, 162.7, 172.0, 220.1, 260.7, 277.2, 301.1, 317.3, 334.1, 340.2, 349.7, 358.0, 363.5, 380.5, 402.8, 415.2, 424.3, 426.6, 427.8, 431.0, 456.4, 472.9, 480.9, 521.1, 563.4, 578.2, 597.8],
        theoretical_spectrum_of_cyclic_peptide_with_noisy_aminoacid_masses([57], get_unique_amino_acid_masses_as_dict(), 0.6)
    )
    print(f'{s}')
    s = score_spectrums(
        [0.1, 56.8, 153.9, 162.7, 172.0, 220.1, 260.7, 277.2, 301.1, 317.3, 334.1, 340.2, 349.7, 358.0, 363.5, 380.5, 402.8, 415.2, 424.3, 426.6, 427.8, 431.0, 456.4, 472.9, 480.9, 521.1, 563.4, 578.2, 597.8],
        theoretical_spectrum_of_cyclic_peptide_with_noisy_aminoacid_masses([57, 57], get_unique_amino_acid_masses_as_dict(), 0.6)
    )
    print(f'{s}')
    s = score_spectrums(
        [0.1, 56.8, 153.9, 162.7, 172.0, 220.1, 260.7, 277.2, 301.1, 317.3, 334.1, 340.2, 349.7, 358.0, 363.5, 380.5, 402.8, 415.2, 424.3, 426.6, 427.8, 431.0, 456.4, 472.9, 480.9, 521.1, 563.4, 578.2, 597.8],
        theoretical_spectrum_of_cyclic_peptide_with_noisy_aminoacid_masses([154.0, 107.0, 154.0, 57.0, 91.0], {154: 154, 107: 107, 57: 57, 91: 91}, 0.6)
    )
    print(f'{s}')
