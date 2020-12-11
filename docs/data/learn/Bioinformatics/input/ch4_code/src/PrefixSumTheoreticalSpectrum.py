from itertools import accumulate
from typing import List, TypeVar, Dict

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

# MARKDOWN
def theoretical_spectrum(peptide: List[AA], mass_table: Dict[AA, float], cyclic: bool) -> List[int]:
    prefixsum_masses = list(accumulate([mass_table[aa] for aa in peptide], initial=0.0))
    ret = [0.0]
    for end_idx in range(0, len(prefixsum_masses)):
        for start_idx in range(0, end_idx):
            min_mass = prefixsum_masses[start_idx]
            max_mass = prefixsum_masses[end_idx]
            ret.append(max_mass - min_mass)
            if cyclic and start_idx > 0 and end_idx < len(peptide):
                ret.append(prefixsum_masses[-1] - (prefixsum_masses[end_idx] - prefixsum_masses[start_idx]))
    ret.sort()
    return ret
# MARKDOWN


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        peptide = input().strip()
        type = input().strip()
        mass_table = {e.strip().split(':')[0]: float(e.strip().split(':')[1]) for e in input().strip().split(',')}
        spectrum = theoretical_spectrum(
            list(peptide),
            mass_table,
            {'cyclic': True, 'linear': False}[type]
        )
        print(f'The theoretical spectrum for the {type} peptide {peptide} is {spectrum}', end="\n\n")
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()