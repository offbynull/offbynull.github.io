from typing import List, Dict, Tuple

from NoisyMassesLeaderboard import Leaderboard
from NoisyMassesScoreSpectrums import score_spectrums
from NoisyMassesScoreSpectrums import theoretical_spectrum_of_cyclic_peptide_with_noisy_aminoacid_masses
from Utils import T


class TopPeptidesTracker:
    def __init__(self, exp_spec: List[float], mass_table: Dict[T, float], amino_acid_mass_tolerance: float, max_backlog=1):
        assert max_backlog >= 1
        self.mass_table = mass_table
        self.exp_spec = exp_spec
        self.mass_table = mass_table
        self.amino_acid_mass_tolerance = amino_acid_mass_tolerance
        self.max_backlog = max_backlog
        self.leader_peptides_top_score = 0
        self.leader_peptides = {0: []}

    def add(self, peptide: List[float]) -> None:
        peptide_theo_spec = theoretical_spectrum_of_cyclic_peptide_with_noisy_aminoacid_masses(
            peptide,
            self.mass_table,
            self.amino_acid_mass_tolerance
        )
        peptide_score = score_spectrums(self.exp_spec, peptide_theo_spec)
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
        cyclopeptide_experimental_spectrum: List[float],
        n: int,
        mass_table: Dict[T, float],
        mass_ranges: List[Tuple[float, float]],
        amino_acid_mass_tolerance: float,
        top_peptides_max_backlog: int
) -> Dict[Tuple[float, float], Dict[int, List[List[T]]]]:
    cyclopeptide_experimental_spectrum.sort()  # Just in case -- it should already be sorted

    leaderboard = Leaderboard(cyclopeptide_experimental_spectrum, mass_table, amino_acid_mass_tolerance)
    top_peptide_bins = dict([(mr, TopPeptidesTracker(cyclopeptide_experimental_spectrum, mass_table, top_peptides_max_backlog)) for mr in mass_ranges])
    while len(leaderboard) > 0:
        # Branch
        leaderboard.expand()
        # Bound
        filtered = leaderboard.filter_based_on_mass(mass_ranges)
        for mr, peptides in filtered.items():
            top_peptides = top_peptide_bins[mr]
            for p in peptides:
                top_peptides.add(p)
        leaderboard.trim(n)

    return dict([(mr, top_peptides.dump()) for mr, top_peptides in top_peptide_bins.items()])