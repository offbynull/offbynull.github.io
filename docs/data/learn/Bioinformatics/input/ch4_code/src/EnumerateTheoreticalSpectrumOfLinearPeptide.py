from typing import List

from Utils import get_amino_acid_to_mass_table


def enumerate_theoretical_spectrum_of_linear_peptide(peptide: str, mass_table=None) -> List[int]:
    if mass_table is None:
        mass_table = get_amino_acid_to_mass_table()

    prefix_masses = [0]
    for i, ch in enumerate(peptide):
        prev_mass = prefix_masses[i]
        next_mass = prev_mass + mass_table[ch]
        prefix_masses.append(next_mass)

    ret = [0]
    for k_end in range(0, len(prefix_masses)):
        for k_start in range(0, k_end):
            min_mass = prefix_masses[k_start]
            max_mass = prefix_masses[k_end]
            ret.append(max_mass - min_mass)

    ret.sort()
    return ret
