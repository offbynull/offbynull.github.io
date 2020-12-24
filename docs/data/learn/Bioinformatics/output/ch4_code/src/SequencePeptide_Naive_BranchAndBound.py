from typing import List, Dict, TypeVar

from PeptideType import PeptideType
from TheoreticalSpectrum_PrefixSum import theoretical_spectrum
from helpers.Utils import contains_all_sorted

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
        # Branch candidates
        new_candidate_peptides = []
        for p in candidate_peptides:
            for m in aa_mass_table:
                new_p = p[:] + [m]
                new_candidate_peptides.append(new_p)
        candidate_peptides = new_candidate_peptides
        # Test candidates to see if they match exp_spec or if they should keep being branched
        removal_idxes = set()
        for i, p in enumerate(candidate_peptides):
            p_mass = sum([aa_mass_table[aa] for aa in p])
            if p_mass == peptide_mass:
                theo_spec = theoretical_spectrum(p, peptide_type, aa_mass_table)
                if theo_spec == exp_spec:
                    final_peptides.append(p)
                removal_idxes.add(i)
            else:
                # Why get the theo spec of the linear version even if the peptide is cyclic? Think about what's
                # happening here. If the exp spec is for cyclic peptide NQYQ, and you're checking to see if the
                # candidate NQY should continue to be branched out...
                #
                # Exp spec  cyclic NQYQ: [0, 114, 128, 128, 163, 242, 242,      291, 291, 370, 405, 405, 419, 533]
                # Theo spec cyclic NQY:  [0, 114, 128,      163, 242,      277, 291,           405]
                #                                                           ^
                #                                                           |
                #                                                        mass(YN)
                #
                # Since NQY is being treated as a cyclic peptide, it has the subpeptide YN (mass of 277). However, the
                # cyclic peptide NQYQ doesn't have the subpeptide YN. That means NQY won't be branched out any further
                # even though it should. As such, even if the exp spec is for a cyclic peptide, treat the candidates as
                # linear segments of that cyclic peptide (essentially linear peptides).
                #
                # Exp spec  cyclic NQYQ: [0, 114, 128, 128, 163, 242, 242, 291, 291, 370, 405, 405, 419, 533]
                # Theo spec linear NQY:  [0, 114, 128,      163, 242,      291,           405]
                #
                # Given the specs above, the exp spec contains all masses in the theo spec.
                theo_spec = theoretical_spectrum(p, PeptideType.LINEAR, aa_mass_table)
                if not contains_all_sorted(theo_spec, exp_spec):
                    removal_idxes.add(i)
        candidate_peptides = [p for i, p in enumerate(candidate_peptides) if i not in removal_idxes]
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
