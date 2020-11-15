from typing import List, Dict, Callable

from FuzzyScoreSpectrums2 import score_spectrums
from Leaderboard import Leaderboard
from TheoreticalSpectrumOfCyclicPeptide import theoretical_spectrum_of_cyclic_peptide
from Utils import get_amino_acid_to_mass_table, T, N


class TopPeptidesTracker:
    def __init__(self, exp_spec: List[N], mass_table: Dict[T, N], score_func: Callable[[List[N], List[N]], int], max_backlog=1):
        assert max_backlog >= 1
        self.mass_table = mass_table
        self.exp_spec = exp_spec
        self.ass_table = mass_table
        self.score_func = score_func
        self.max_backlog = max_backlog
        self.leader_peptides_top_score = 0
        self.leader_peptides = {0: []}

    def add(self, peptide: List[N]) -> None:
        peptide_theo_spec = theoretical_spectrum_of_cyclic_peptide(peptide, mass_table=self.mass_table)
        peptide_score = self.score_func(peptide_theo_spec, self.exp_spec)
        min_acceptable_score = self.leader_peptides_top_score - self.max_backlog
        if peptide_score < min_acceptable_score:
            return
        leaders = self.leader_peptides.setdefault(peptide_score, [])
        leaders.append(peptide)
        if peptide_score > self.leader_peptides_top_score:
            self.leader_peptides_top_score = peptide_score
            if len(self.leader_peptides) > self.max_backlog:
                smallest_leader_score = min(self.leader_peptides.keys())
                self.leader_peptides.pop(smallest_leader_score)

    def dump(self) -> Dict[int, List[List[T]]]:
        return self.leader_peptides.copy()


def sequence_cyclic_peptide(
        cyclopeptide_experimental_spectrum: List[N],
        n: int,
        mass_table: Dict[T, N],
        score_func: Callable[[List[N], List[N]], int],
        final_mass_tolerance: N,
        top_peptides_max_backlog: int
) -> Dict[int, List[List[T]]]:
    cyclopeptide_experimental_spectrum.sort()  # Just in case -- it should already be sorted
    cyclopeptide_experimental_mass = cyclopeptide_experimental_spectrum[-1]
    upper_allowable_mass = cyclopeptide_experimental_mass + final_mass_tolerance
    lower_allowable_mass = cyclopeptide_experimental_mass - final_mass_tolerance

    leaderboard = Leaderboard(cyclopeptide_experimental_spectrum, mass_table, score_func)
    top_peptides = TopPeptidesTracker(cyclopeptide_experimental_spectrum, mass_table, score_func, top_peptides_max_backlog)
    while len(leaderboard) > 0:
        # Branch
        leaderboard.expand()
        # Bound
        filtered = leaderboard.filter_based_on_mass(lower_allowable_mass, upper_allowable_mass)
        [top_peptides.add(p) for p in filtered]
        leaderboard.trim(n)

    return top_peptides.dump()


if __name__ == '__main__':
    mass_table = dict([(k, float(v)) for k, v in get_amino_acid_to_mass_table().items()])
    actual_seq = sequence_cyclic_peptide(
        theoretical_spectrum_of_cyclic_peptide('NQEL', mass_table=mass_table),
        10,
        mass_table,
        score_func=score_spectrums
    )
    print(f'{actual_seq}')