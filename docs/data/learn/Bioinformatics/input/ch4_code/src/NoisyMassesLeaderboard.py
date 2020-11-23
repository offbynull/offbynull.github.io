from typing import List, Dict, Callable, Tuple

from NoisyMassesScoreSpectrums import theoretical_spectrum_of_cyclic_peptide_with_noisy_aminoacid_masses, \
    score_spectrums
from TheoreticalSpectrumOfLinearPeptide import theoretical_spectrum_of_linear_peptide
from Utils import T


# Score a set of peptides against an experimental spectrum and return the top n (including ties at the end, so it may be
# end up being more than n).
class Leaderboard:
    def __init__(self, exp_spec: List[float], mass_table: Dict[T, float], amino_acid_mass_tolerance: float):
        self.exp_spec = exp_spec
        self.mass_table = mass_table
        self.amino_acid_mass_tolerance = amino_acid_mass_tolerance
        self.peptides = [[]]

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

        spectrums = [theoretical_spectrum_of_cyclic_peptide_with_noisy_aminoacid_masses(p, self.mass_table, self.amino_acid_mass_tolerance) for p in self.peptides]
        scores = [score_spectrums(self.exp_spec, s) for s in spectrums]
        sorted_peptide_scores = list(sorted(zip(self.peptides, scores), key=lambda x: x[1], reverse=True))

        # Sorted biggest to smallest...
        # Return first n elements from sorted_peptide_scores, but since we're including ending ties we need to check if
        # the element at n repeats. If it does, include the repeats (the result wil be larger than n).
        for j in range(n + 1, len(sorted_peptide_scores)):
            if sorted_peptide_scores[n][1] > sorted_peptide_scores[j][1]:
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