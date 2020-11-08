from typing import List, Optional, Dict, Set, TypeVar

from ScoreSpectrums import score_spectrums, top_n_peptides_including_last_place_ties
from TheoreticalSpectrumOfCyclicPeptide import theoretical_spectrum_of_cyclic_peptide
from TheoreticalSpectrumOfLinearPeptide import theoretical_spectrum_of_linear_peptide
from Utils import HashableList, contains_all_sorted, get_amino_acid_to_mass_table

T = TypeVar('T')


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