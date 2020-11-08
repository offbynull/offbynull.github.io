from typing import List

from Utils import get_amino_acid_to_mass_table


def enumerate_theoretical_spectrum_of_cyclic_peptide(peptide: str, mass_table=None) -> List[int]:
    if mass_table is None:
        mass_table = get_amino_acid_to_mass_table()

    # THIS IS THE BRUTEFORCE METHOD. IT WORKS JUST FINE.
    # # prepopulate with weight for subpeptide of length 0 and subpeptide of length n (the entire the peptide)
    # ret = [
    #     0,
    #     sum([mass_table[ch] for ch in data])
    # ]
    #
    # for k in range(1, len(data)):
    #     for subpeptide, _ in slide_window(data, k, cyclic=True):
    #         ret.append(sum([mass_table[ch] for ch in subpeptide]))
    #
    # ret.sort()
    # print(f'{" ".join([str(i) for i in ret])}')

    # THIS IS THE CLEVER METHOD
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
            if k_start > 0 and k_end < len(peptide):
                ret.append(prefix_masses[-1] - (prefix_masses[k_end] - prefix_masses[k_start]))

    ret.sort()
    return ret
