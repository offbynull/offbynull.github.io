from typing import List, Dict, TypeVar

from TheoreticalSpectrum_PrefixSum import theoretical_spectrum, PeptideType

AA = TypeVar('AA')


# MARKDOWN
def sequence_peptide(
        exp_spec: List[float],  # must be sorted asc
        peptide_type: PeptideType,
        aa_mass_table: Dict[AA, float]
) -> List[List[AA]]:
    peptide_mass = exp_spec[-1]
    candidate_peptides = [[]]
    final_peptides = []
    while len(candidate_peptides) > 0:
        new_candidate_peptides = []
        for p in candidate_peptides:
            for m in aa_mass_table.keys():
                new_p = p[:] + [m]
                new_p_mass = sum([aa_mass_table[aa] for aa in new_p])
                if new_p_mass == peptide_mass and theoretical_spectrum(new_p, peptide_type, aa_mass_table) == exp_spec:
                    final_peptides.append(new_p)
                elif new_p_mass < peptide_mass:
                    new_candidate_peptides.append(new_p)
        candidate_peptides = new_candidate_peptides
    return final_peptides
# MARKDOWN


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        exp_spec = [float(m) for m in input().strip().split()]
        peptide_type = input().strip()
        mass_table = {e.strip().split(':')[0]: float(e.strip().split(':')[1]) for e in input().strip().split(',')}
        peptides = sequence_peptide(
            exp_spec,
            {'cyclic': PeptideType.CYCLIC, 'linear': PeptideType.LINEAR}[peptide_type],
            mass_table
        )
        print(f'The {peptide_type} peptides matching the experimental spectrum {exp_spec} are...', end="\n\n")
        for peptide in peptides:
            print(f' * {"".join(peptide)}')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()
