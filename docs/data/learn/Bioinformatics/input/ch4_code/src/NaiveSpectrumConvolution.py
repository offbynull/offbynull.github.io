from collections import Counter
from typing import List

from PrefixSumTheoreticalSpectrum import theoretical_spectrum, PeptideType
from helpers.AminoAcidUtils import get_amino_acid_to_mass_table


# MARKDOWN
def spectrum_convolution(experimental_spectrum: List[float], min_mass=57.0, max_mass=200.0) -> List[float]:
    # it's expected that experimental_spectrum is sorted smallest to largest
    diffs = []
    for row_idx, row_mass in enumerate(experimental_spectrum):
        for col_idx, col_mass in enumerate(experimental_spectrum):
            mass_diff = row_mass - col_mass
            if min_mass <= mass_diff <= max_mass:
                diffs.append(mass_diff)
    diffs.sort()
    return diffs
# MARKDOWN


if __name__ == '__main__':
    spectrum = theoretical_spectrum(list('NQEL'), PeptideType.CYCLIC, get_amino_acid_to_mass_table())
    differences = spectrum_convolution(spectrum)

    count = Counter(differences)
    print(f'{count}')
