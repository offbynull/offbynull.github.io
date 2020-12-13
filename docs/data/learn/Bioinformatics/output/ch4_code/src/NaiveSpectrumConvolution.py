from collections import Counter
from typing import List

from TheoreticalSpectrumOfCyclicPeptide import theoretical_spectrum_of_cyclic_peptide


def spectrum_convolution(experimental_spectrum: List[int], min_mass=57, max_mass=200) -> List[int]:
    # it's expected that experimental_spectrum is sorted smallest to largest
    diffs = []
    for row_idx, row_mass in enumerate(experimental_spectrum):
        for col_idx, col_mass in enumerate(experimental_spectrum):
            mass_diff = row_mass - col_mass
            if min_mass <= mass_diff <= max_mass:
                diffs.append(mass_diff)
    diffs.sort()
    return diffs


if __name__ == '__main__':
    spectrum = theoretical_spectrum_of_cyclic_peptide('NQEL')
    differences = spectrum_convolution(spectrum)

    count = Counter(differences)
    print(f'{count}')
