from typing import List, TypeVar, Dict

from helpers.AminoAcidUtils import get_amino_acid_to_mass_table
from helpers.Utils import slide_window

AA = TypeVar('AA')


# MARKDOWN
def theoretical_spectrum(peptide: List[AA], mass_table: Dict[AA, float], cyclic: bool) -> List[int]:
    # add subpeptide of length 0's mass
    ret = [0]
    # add subpeptide of length 1 to k-1's mass
    for k in range(1, len(peptide)):
        for subpeptide, _ in slide_window(peptide, k, cyclic=cyclic):
            ret.append(sum([mass_table[ch] for ch in subpeptide]))
    # add subpeptide of length k's mass
    ret.append(sum([mass_table[aa] for aa in peptide]))
    # sort and return
    ret.sort()
    return ret
# MARKDOWN


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        peptide = input().strip()
        type = input().strip()
        spectrum = theoretical_spectrum(
            list(peptide),
            get_amino_acid_to_mass_table(),
            {'cyclic': True, 'linear': False}[type]
        )
        print(f'The theoretical spectrum for the {type} peptide {peptide} is {spectrum}', end="\n\n")
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()