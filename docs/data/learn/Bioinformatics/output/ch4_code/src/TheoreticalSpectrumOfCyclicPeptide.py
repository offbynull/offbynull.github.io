from itertools import accumulate
from typing import List, TypeVar, Union

from Utils import get_amino_acid_to_mass_table

T = TypeVar('T')


def theoretical_spectrum_of_cyclic_peptide(peptide: Union[str, List[T]], mass_table=None) -> List[int]:
    if mass_table is None:
        mass_table = get_amino_acid_to_mass_table()

    if isinstance(peptide, str):
        peptide = [ch for ch in peptide]

    #
    # THIS IS THE BRUTEFORCE METHOD. IT WORKS JUST FINE AND ISN'T ALL THAT SLOW.
    #

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
    # THIS IS THE CLEVER METHOD
    #

    # This line calculates the cumulative sum of the peptid masses
    # e.g. amino acid masses of peptide GASP is [57, 71, 87, 97], which has the cumulative sum of....
    #        [0,        0+57,      0+57+71,    0+57+71+87,  0+57+71+87+97]
    #      = [0,        57,        128,        215,         312          ]
    #      = [mass(''), mass('G'), mass('GA'), mass('GAS'), mass('GASP') ]
    cumsum_masses = list(accumulate([mass_table[aa] for aa in peptide], initial=0))

    # Use the cumulative sum to calculate subpeptide masses. For example, the mass of the subpeptide...
    #      mass('GASP') = mass('GASP') - mass('')    = cumsum_masses[4] - cumsum_masses[0]
    #      mass('ASP')  = mass('GASP') - mass('G')   = cumsum_masses[4] - cumsum_masses[1]
    #      mass('AS')   = mass('GAS')  - mass('G')   = cumsum_masses[3] - cumsum_masses[1]
    #      mass('A')    = mass('GA')   - mass('G')   = cumsum_masses[2] - cumsum_masses[1]
    #      mass('S')    = mass('GAS')  - mass('GA')  = cumsum_masses[3] - cumsum_masses[2]
    #      mass('P')    = mass('GASP') - mass('GAS') = cumsum_masses[4] - cumsum_masses[3]
    #      etc...
    #
    # Because this is a cyclic peptide, there are subpeptides that wrap around:
    #   G---->A
    #   ^     |
    #   |     v
    #   P<----S
    # For example, PG is a valid subpeptide. The cumulative sum can be used to calculate these wrapping subpeptides as
    # well....
    #      mass('PG') = mass('GASP') - mass('AS')
    #                 = mass('GASP') - (mass('GAS') - mass('G'))    # SUBSTITUTE IN mass('AS') EXAMPLE FROM ABOVE
    #                 = cumsum_masses[4] - (cumsum_masses[3] - cumsum_masses[1])
    ret = [0]
    for k_end in range(0, len(cumsum_masses)):
        for k_start in range(0, k_end):
            min_mass = cumsum_masses[k_start]
            max_mass = cumsum_masses[k_end]
            ret.append(max_mass - min_mass)
            if k_start > 0 and k_end < len(peptide):
                ret.append(cumsum_masses[-1] - (cumsum_masses[k_end] - cumsum_masses[k_start]))

    ret.sort()
    return ret


if __name__ == '__main__':
    x = theoretical_spectrum_of_cyclic_peptide('GASP')
    print(f'{x}')