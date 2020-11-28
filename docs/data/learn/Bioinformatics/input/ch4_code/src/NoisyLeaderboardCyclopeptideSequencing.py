from typing import List, Dict, Tuple, Optional

from NoisyScoreSpectrums import score_spectrums, \
    theoretical_spectrum_of_linear_peptide_with_noisy_aminoacid_masses
from NoisyScoreSpectrums import theoretical_spectrum_of_cyclic_peptide_with_noisy_aminoacid_masses
from Utils import T


# Score a set of peptides against an experimental spectrum and return the top n (including ties at the end, so it may be
# end up being more than n).
class Leaderboard:
    def __init__(
            self,
            exp_spec: List[float],
            mass_table: Dict[T, float],
            amino_acid_mass_tolerance: float,
            initial_peptides: Optional[List[List[T]]] = None
    ):
        self.exp_spec = exp_spec
        self.mass_table = mass_table
        self.amino_acid_mass_tolerance = amino_acid_mass_tolerance
        if initial_peptides is None:
            self.peptides = [[]]
        else:
            self.peptides = initial_peptides[:]

    def expand(self):
        expanded_peptides = []
        for p in self.peptides:
            for m in self.mass_table:
                new_p = p[:]
                new_p.append(m)
                expanded_peptides.append(new_p)
        self.peptides = expanded_peptides

    # Trim to top n peptides including last place ties
    def trim(self, n: int):
        if len(self.peptides) == 0:
            return

        scores = [(0, 0.0)] * len(self.peptides)
        for i, peptide in enumerate(self.peptides):
            theo_spec = theoretical_spectrum_of_linear_peptide_with_noisy_aminoacid_masses(
                peptide,
                self.mass_table,
                self.amino_acid_mass_tolerance
            )
            score = score_spectrums(self.exp_spec, theo_spec)
            score_within = score[0]
            score_perc = score[2]
            scores[i] = (score_within, score_perc)
        sorted_peptide_scores = list(sorted(zip(self.peptides, scores), key=lambda x: x[1], reverse=True))

        # Sorted biggest to smallest...
        # Return first n elements from sorted_peptide_scores, but since we're including ending ties we need to check if
        # the element at n repeats. If it does, include the repeats (the result wil be larger than n).
        for j in range(n + 1, len(sorted_peptide_scores)):
            n_score_within = sorted_peptide_scores[n][1][0]
            j_score_within = sorted_peptide_scores[j][1][0]
            if n_score_within > j_score_within:
                self.peptides = [p for p, _ in sorted_peptide_scores[:j - 1]]
                return
        self.peptides = [p for p, _ in sorted_peptide_scores]

    # Filter out peptides that have a mass in some range
    def filter_based_on_mass(self, mass_ranges: List[Tuple[float, float]]) -> Dict[Tuple[float, float], List[List[T]]]:
        max_mass = max([mass_range[1] for mass_range in mass_ranges])
        filtered = dict([(mass_range, []) for mass_range in mass_ranges])
        new_peptides = []
        for i in range(len(self.peptides) - 1, -1, -1):  # walk indices backwards
            p = self.peptides.pop(i)
            p_mass = sum([self.mass_table[aa] for aa in p])
            if p_mass > max_mass:
                continue
            for filter_mass_range, filter_peptides in filtered.items():
                range_min_mass, range_max_mass = filter_mass_range
                if range_min_mass <= p_mass <= range_max_mass:
                    filter_peptides.append(p)
            new_peptides.append(p)
        self.peptides = new_peptides
        return filtered

    def dump(self) -> List[List[T]]:
        return self.peptides.copy()

    def __len__(self) -> int:
        return len(self.peptides)


class TopPeptides:
    def __init__(
            self,
            exp_spec: List[float],
            mass_table: Dict[T, float],
            amino_acid_mass_tolerance: float,
            max_backlog: int = 1
    ):
        self.mass_table = mass_table
        self.exp_spec = exp_spec
        self.mass_table = mass_table
        self.amino_acid_mass_tolerance = amino_acid_mass_tolerance
        self.max_backlog = max_backlog
        self.leader_peptides_top_score = 0
        self.leader_peptides = {0: []}

    def add(
            self,
            peptide: List[float]
    ) -> None:
        peptide_theo_spec = theoretical_spectrum_of_cyclic_peptide_with_noisy_aminoacid_masses(
            peptide,
            self.mass_table,
            self.amino_acid_mass_tolerance
        )
        peptide_score = score_spectrums(self.exp_spec, peptide_theo_spec)[0]
        min_acceptable_score = self.leader_peptides_top_score - self.max_backlog
        if peptide_score < min_acceptable_score:
            return
        leaders = self.leader_peptides.setdefault(peptide_score, [])
        leaders.append(peptide)
        if peptide_score > self.leader_peptides_top_score:
            self.leader_peptides_top_score = peptide_score
            if len(self.leader_peptides) >= self.max_backlog:
                smallest_leader_score = min(self.leader_peptides.keys())
                self.leader_peptides.pop(smallest_leader_score)

    def dump(self) -> List[List[T]]:
        return [p for peptides in self.leader_peptides.values() for p in peptides]


def sequence_cyclic_peptide(
        cyclopeptide_experimental_spectrum: List[float],
        n: int,
        mass_table: Dict[T, float],
        mass_ranges: List[Tuple[float, float]],
        amino_acid_mass_tolerance: float,
        allowable_trailing: int,
        initial_peptides: Optional[List[List[T]]] = None
) -> Dict[Tuple[float, float], List[List[T]]]:
    cyclopeptide_experimental_spectrum.sort()  # Just in case -- it should already be sorted

    leaderboard = Leaderboard(
        cyclopeptide_experimental_spectrum,
        mass_table,
        amino_acid_mass_tolerance,
        initial_peptides
    )
    top_peptide_bins = {mr: TopPeptides(cyclopeptide_experimental_spectrum, mass_table, amino_acid_mass_tolerance, allowable_trailing) for mr in mass_ranges}
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

    return {mr: top_peptides.dump() for mr, top_peptides in top_peptide_bins.items()}
