from typing import List

from PeptideType import PeptideType


# MARKDOWN
def theoretical_spectrum_tolerances(
        peptide_len: int,
        peptide_type: PeptideType,
        amino_acid_mass_tolerance: float
) -> List[float]:
    ret = [0.0]
    if peptide_type == PeptideType.LINEAR:
        for i in range(peptide_len):
            tolerance = (i + 1) * amino_acid_mass_tolerance
            ret += [tolerance] * (peptide_len - i)
    elif peptide_type == PeptideType.CYCLIC:
        for i in range(peptide_len - 1):
            tolerance = (i + 1) * amino_acid_mass_tolerance
            ret += [tolerance] * peptide_len
        if peptide_len != 0:
            ret.append(peptide_len * amino_acid_mass_tolerance)
    else:
        raise ValueError()
    return ret
# MARKDOWN


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        peptide = input().strip()
        peptide_type = input().strip()
        amino_acid_mass_tolerance = float(input().strip())
        tolerances = theoretical_spectrum_tolerances(
            len(peptide),
            {'cyclic': PeptideType.CYCLIC, 'linear': PeptideType.LINEAR}[peptide_type],
            amino_acid_mass_tolerance
        )
        print(f'The theoretical spectrum for {peptide_type} peptide {peptide} with amino acid mass'
              f' tolerance of {amino_acid_mass_tolerance}...', end="\n\n")
        print(f'{tolerances}', end="\n\n")
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()