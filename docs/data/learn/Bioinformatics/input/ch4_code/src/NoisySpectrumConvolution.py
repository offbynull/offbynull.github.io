import typing
from collections import Counter
from typing import List

from TheoreticalSpectrumOfCyclicPeptide import theoretical_spectrum_of_cyclic_peptide


def group_fuzzy_convolution_matches(masses: List[float], tolerance: float) -> typing.Counter[float]:
    masses = sorted(masses)
    length = len(masses)
    ret = Counter()
    for i, m1 in enumerate(masses):
        if m1 in ret:
            continue
        # search backwards
        left_limit = 0
        for j in range(i, -1, -1):
            m2 = masses[j]
            if abs(m2 - m1) > tolerance:
                break
            left_limit = j
        # search forwards
        right_limit = length - 1
        for j in range(i, length):
            m2 = masses[j]
            if abs(m2 - m1) > tolerance:
                break
            right_limit = j
        count = right_limit - left_limit
        ret[m1] = count
    return ret


def spectrum_convolution(experimental_spectrum: List[float], tolerance: float, min_mass=57.0, max_mass=200.0, round_digits=-1) -> typing.Counter[float]:
    min_mass -= tolerance
    max_mass += tolerance

    # it's expected that experimental_spectrum is sorted smallest to largest
    diffs = []
    for row_idx, row_mass in enumerate(experimental_spectrum):
        for col_idx, col_mass in enumerate(experimental_spectrum):
            mass_diff = row_mass - col_mass
            if round_digits != -1:
                mass_diff = round(mass_diff, round_digits)
            if min_mass <= mass_diff <= max_mass:
                diffs.append(mass_diff)

    return group_fuzzy_convolution_matches(diffs, tolerance)


if __name__ == '__main__':
    spectrum = theoretical_spectrum_of_cyclic_peptide('NQEL')
    differences = spectrum_convolution(spectrum)

    count = Counter(differences)
    print(f'{count}')
