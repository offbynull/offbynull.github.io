from enum import Enum
from itertools import accumulate
from typing import List, TypeVar, Dict, Tuple

AA = TypeVar('AA')


# Calculates the prefix sum of peptide masses
# e.g. amino acid masses of peptide GASP is [57, 71, 87, 97], which has the cumulative sum of....
#        [0,        0+57,      0+57+71,    0+57+71+87,  0+57+71+87+97]
#      = [0,        57,        128,        215,         312          ]
#      = [mass(''), mass('G'), mass('GA'), mass('GAS'), mass('GASP') ]
#
# Then, use the prefix sum to calculate subpeptide masses. For example, the mass of the subpeptide...
#      mass('GASP') = mass('GASP') - mass('')    = prefixsum_masses[4] - prefixsum_masses[0]
#      mass('ASP')  = mass('GASP') - mass('G')   = prefixsum_masses[4] - prefixsum_masses[1]
#      mass('AS')   = mass('GAS')  - mass('G')   = prefixsum_masses[3] - prefixsum_masses[1]
#      mass('A')    = mass('GA')   - mass('G')   = prefixsum_masses[2] - prefixsum_masses[1]
#      mass('S')    = mass('GAS')  - mass('GA')  = prefixsum_masses[3] - prefixsum_masses[2]
#      mass('P')    = mass('GASP') - mass('GAS') = prefixsum_masses[4] - prefixsum_masses[3]
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
#                 = prefixsum_masses[4] - (prefixsum_masses[3] - prefixsum_masses[1])


class PeptideType(Enum):
    LINEAR = 0
    CYCLIC = 1


# MARKDOWN
def to_mass_range(
        subpeptide_len: int,
        subpeptide_mass: int,
        amino_acid_mass_tolerance: float
) -> Tuple[float, float, float]:
    max_noise = subpeptide_len * amino_acid_mass_tolerance
    min_subpeptide_mass = subpeptide_mass - max_noise
    max_subpeptide_mass = subpeptide_mass + max_noise
    return subpeptide_mass, min_subpeptide_mass, max_subpeptide_mass


def theoretical_spectrum(
        peptide: List[AA],
        peptide_type: PeptideType,
        amino_acid_mass_tolerance: float,
        mass_table: Dict[AA, float]
) -> List[Tuple[float, float, float]]:
    prefixsum_masses = list(accumulate([mass_table[aa] for aa in peptide], initial=0.0))
    ret = [(0.0, 0.0, 0.0)]
    for end_idx in range(0, len(prefixsum_masses)):
        for start_idx in range(0, end_idx):
            length = end_idx - start_idx
            min_mass = prefixsum_masses[start_idx]
            max_mass = prefixsum_masses[end_idx]
            mass = max_mass - min_mass
            mass_range = to_mass_range(length, mass, amino_acid_mass_tolerance)
            ret.append(mass_range)
            if peptide_type == PeptideType.CYCLIC and start_idx > 0 and end_idx < len(peptide):
                mass = prefixsum_masses[-1] - (prefixsum_masses[end_idx] - prefixsum_masses[start_idx])
                mass_range = to_mass_range(length, mass, amino_acid_mass_tolerance)
                ret.append(mass_range)
    ret.sort()
    return ret
# MARKDOWN


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        peptide = input().strip()
        type = input().strip()
        max_noise = float(input().strip())
        mass_table = {e.strip().split(':')[0]: float(e.strip().split(':')[1]) for e in input().strip().split(',')}
        spectrum = theoretical_spectrum(
            list(peptide),
            {'cyclic': PeptideType.CYCLIC, 'linear': PeptideType.LINEAR}[type],
            max_noise,
            mass_table
        )
        print(f'The theoretical spectrum for the {type} peptide {peptide} is ...', end="\n\n")
        for m in spectrum:
            print(f' * {m}', end="\n")
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()