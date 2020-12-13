from typing import List, Optional, Dict, TypeVar

from NaiveSpectrumScore import score_spectrums
from TheoreticalSpectrumOfCyclicPeptide import theoretical_spectrum_of_cyclic_peptide
from TheoreticalSpectrumOfLinearPeptide import theoretical_spectrum_of_linear_peptide
from helpers.AminoAcidUtils import get_amino_acid_to_mass_table

T = TypeVar('T')


# Score a set of peptides against a reference spectrum and return the top n (including ties at the end, so it may be end
# up being more than n).
def top_n_peptides_including_last_place_ties(
        peptides: List[List[T]],
        reference_spectrum: List[int],
        n: int,
        mass_table=None
) -> List[List[T]]:
    if len(peptides) == 0:
        return peptides

    spectrums = [theoretical_spectrum_of_linear_peptide(p, mass_table) for p in peptides]
    scores = [score_spectrums(s, reference_spectrum) for s in spectrums]
    sorted_peptide_scores = list(sorted(zip(peptides, scores), key=lambda x: x[1], reverse=True))  # big to small

    # Return first n elements from sorted_peptide_scores, but since we're including ending ties we need to check if the
    # element at n repeats. If it does, include the repeats (the result wil be larger than n).
    for j in range(n + 1, len(sorted_peptide_scores)):
        if sorted_peptide_scores[n][1] > sorted_peptide_scores[j][1]:
            return [p for p, _ in sorted_peptide_scores[:j-1]]
    return [p for p, _ in sorted_peptide_scores]



def sequence_cyclic_peptide(
        cyclopeptide_experimental_spectrum: List[int],
        n: int,
        mass_table: Optional[Dict[T, int]] = None
) -> List[List[T]]:
    if mass_table is None:
        mass_table = get_amino_acid_to_mass_table()

    cyclopeptide_experimental_spectrum.sort()  # Just in case -- it should already be sorted
    cyclopeptide_experimental_mass = cyclopeptide_experimental_spectrum[-1]

    leaderboard = [[]]
    leader_peptide = next(iter(leaderboard))
    leader_peptides = [leader_peptide]
    while len(leaderboard) > 0:
        # Branch
        new_leaderboard = []
        for p in leaderboard:
            for m in mass_table:
                new_p = p[:]
                new_p.append(m)
                new_leaderboard.append(new_p)
        leaderboard = new_leaderboard
        # Bound
        new_leaderboard = []
        for p in leaderboard:
            p_mass = sum([mass_table[aa] for aa in p])
            if p_mass > cyclopeptide_experimental_mass:
                continue
            elif p_mass == cyclopeptide_experimental_mass:
                p_theoretical_spectrum = theoretical_spectrum_of_cyclic_peptide(p, mass_table=mass_table)
                p_score = score_spectrums(p_theoretical_spectrum, cyclopeptide_experimental_spectrum)
                leader_theoretical_spectrum = theoretical_spectrum_of_cyclic_peptide(leader_peptide,
                                                                                     mass_table=mass_table)
                leader_score = score_spectrums(leader_theoretical_spectrum, cyclopeptide_experimental_spectrum)
                if p_score > leader_score:
                    leader_peptide = p
                    leader_peptides = [p]
                elif p_score == leader_score:
                    leader_peptides.append(p)
            new_leaderboard.append(p)
        leaderboard = new_leaderboard
        leaderboard = top_n_peptides_including_last_place_ties(
            leaderboard,
            cyclopeptide_experimental_spectrum,
            n,
            mass_table=mass_table)
        
    return leader_peptides


if __name__ == '__main__':
    mass_table = get_amino_acid_to_mass_table()
    actual_seq = sequence_cyclic_peptide(
        theoretical_spectrum_of_cyclic_peptide('NQEL', mass_table=mass_table),
        10,
        mass_table=mass_table
    )
    print(f'{actual_seq}')