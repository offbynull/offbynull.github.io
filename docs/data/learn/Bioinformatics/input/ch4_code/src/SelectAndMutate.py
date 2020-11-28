from random import Random
from typing import List, Dict, Tuple, Optional

from NoisyScoreSpectrums import score_spectrums, \
    theoretical_spectrum_of_linear_peptide_with_noisy_aminoacid_masses
from Utils import T, HashableList


class SelectAndMutate:
    def __init__(
            self,
            exp_spec: List[float],
            mass_table: Dict[T, float],
            amino_acid_mass_tolerance: float,
            peptide_len: int,
            population_size: int = 10000,
            population_initial: Optional[List[List[T]]] = None,
            parent_score_fitness_threshold: int = 0,
            random: Optional[Random] = None
    ):
        assert peptide_len >= 0
        assert population_size > 0
        self.exp_spec = exp_spec
        self.mass_table = mass_table
        self.amino_acid_mass_tolerance = amino_acid_mass_tolerance
        self.population_size = population_size
        self.peptides = set()
        self.parent_score_fitness_threshold = parent_score_fitness_threshold
        if random is None:
            random = Random(2)
        self.random = random
        if population_initial is None:
            aas = list(mass_table.keys())
            for j in range(population_size):
                peptide = HashableList([random.choice(aas) for i in range(peptide_len)])
                self.peptides.add(peptide)
        else:
            self.peptides = population_initial

    def select_and_mutate(self):
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

        best_score = sorted_peptide_scores[0][1]
        most_fit = list(
            filter(
                lambda x: x[1][0] >= best_score[0] - self.parent_score_fitness_threshold,
                sorted_peptide_scores
            )
        )
        new_peptides = set()
        aas = list(self.mass_table.keys())
        for i in range(self.population_size):
            parent1 = self.random.choice(most_fit)[0]
            parent2 = self.random.choice(most_fit)[0]
            child = [self.random.choice([a, b]) for a, b in zip(parent1, parent2)]
            child_mutate_count = self.random.randint(0, len(child))
            child_mutate_idxes = self.random.choices(range(len(child)), k=child_mutate_count)
            child_mutated_aas = [self.random.choice(aas) for _ in range(child_mutate_count)]
            for idx, aa in zip(child_mutate_idxes, child_mutated_aas):
                child[idx] = aa
            new_peptides.add(HashableList(child))
        self.peptides = new_peptides

    # Filter out peptides that have a mass in some range
    def filter_based_on_mass(self, mass_ranges: List[Tuple[float, float]]) -> Dict[Tuple[float, float], List[List[T]]]:
        max_mass = max([mass_range[1] for mass_range in mass_ranges])
        filtered = dict([(mass_range, []) for mass_range in mass_ranges])
        new_peptides = set()
        for p in self.peptides.copy():  # walk indices backwards
            p_mass = sum([self.mass_table[aa] for aa in p])
            if p_mass > max_mass:
                continue
            for filter_mass_range, filter_peptides in filtered.items():
                range_min_mass, range_max_mass = filter_mass_range
                if range_min_mass <= p_mass <= range_max_mass:
                    filter_peptides.append(p)
            new_peptides.add(p)
        self.peptides = new_peptides
        return filtered

    def dump(self) -> List[List[T]]:
        return list(self.peptides)

    def __len__(self) -> int:
        return len(self.peptides)
