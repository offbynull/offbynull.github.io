from enum import Enum
from typing import List, Dict, TypeVar, Tuple, Optional

from ExperimentalSpectrumPeptideMassNoise import experimental_spectrum_peptide_mass_noise
from SpectrumConvolution import spectrum_convolution
from SpectrumScore import score_spectrums
from TheoreticalSpectrumTolerances import theoretical_spectrum_tolerances
from TheoreticalSpectrum_PrefixSum import theoretical_spectrum, PeptideType

AA = TypeVar('AA')


class TestResult(Enum):
    MASS_TOO_SMALL = 0
    MASS_TOO_LARGE = 1
    SCORE_TOO_LOW = 2
    ADDED = 3


# MARKDOWN
class SequenceTester:
    def __init__(
            self,
            exp_spec: List[float],           # must be sorted asc
            aa_mass_table: Dict[AA, float],  # amino acid mass table
            aa_mass_tolerance: float,        # amino acid mass tolerance
            peptide_min_mass: float,         # min mass that the peptide could be
            peptide_max_mass: float,         # max mass that the peptide could be
            peptide_type: PeptideType,       # linear or cyclic
            score_backlog: int = 0           # keep this many previous scores
    ):
        self.exp_spec = exp_spec
        self.aa_mass_table = aa_mass_table
        self.aa_mass_tolerance = aa_mass_tolerance
        self.peptide_min_mass = peptide_min_mass
        self.peptide_max_mass = peptide_max_mass
        self.peptide_type = peptide_type
        self.score_backlog = score_backlog
        self.leader_peptides_top_score = 0
        self.leader_peptides = {0: []}

    @staticmethod
    def generate_theroetical_spectrum_with_tolerances(
            peptide: List[AA],
            peptide_type: PeptideType,
            aa_mass_table: Dict[AA, float],
            aa_mass_tolerance: float
    ) -> List[Tuple[float, float, float]]:
        theo_spec_raw = theoretical_spectrum(peptide, peptide_type, aa_mass_table)
        theo_spec_tols = theoretical_spectrum_tolerances(len(peptide), peptide_type, aa_mass_tolerance)
        theo_spec = [(m, m - t, m + t) for m, t in zip(theo_spec_raw, theo_spec_tols)]
        return theo_spec

    def test(
            self,
            peptide: List[AA],
            theo_spec: Optional[List[Tuple[float, float, float]]] = None
    ) -> TestResult:
        if theo_spec is None:
            theo_spec = SequenceTester.generate_theroetical_spectrum_with_tolerances(
                peptide,
                self.peptide_type,
                self.aa_mass_table,
                self.aa_mass_tolerance
            )
        # Don't add if mass out of range
        _, tp_min_mass, tp_max_mass = theo_spec[-1]  # last element of theo spec is the mass of the theo spec peptide
        if tp_min_mass < self.peptide_min_mass:
            return TestResult.MASS_TOO_SMALL
        elif tp_max_mass > self.peptide_max_mass:
            return TestResult.MASS_TOO_LARGE
        # Don't add if the score is lower than the previous n best scores
        peptide_score = score_spectrums(self.exp_spec, theo_spec)[0]
        min_acceptable_score = self.leader_peptides_top_score - self.score_backlog
        if peptide_score < min_acceptable_score:
            return TestResult.SCORE_TOO_LOW
        # Add, but also remove any previous test peptides that are no longer within the acceptable score threshold
        leaders = self.leader_peptides.setdefault(peptide_score, [])
        leaders.append(peptide)
        if peptide_score > self.leader_peptides_top_score:
            self.leader_peptides_top_score = peptide_score
            if len(self.leader_peptides) >= self.score_backlog:
                smallest_leader_score = min(self.leader_peptides.keys())
                self.leader_peptides.pop(smallest_leader_score)
        return TestResult.ADDED
# MARKDOWN


class SequenceTesterSet:
    def __init__(
            self,
            exp_spec: List[float],                           # must be sorted asc
            aa_mass_table: Dict[AA, float],                  # amino acid mass table
            aa_mass_tolerance: float,                        # amino acid mass tolerance
            peptide_mass_ranges: List[Tuple[float, float]],  # min mass that the peptide could be
            peptide_type: PeptideType,                       # linear or cyclic
            score_backlog: int = 0                           # keep this many previous scores
    ):
        testers = []
        for peptide_min_mass, peptide_max_mass in peptide_mass_ranges:
            tester = SequenceTester(
                exp_spec,
                aa_mass_table,
                aa_mass_tolerance,
                peptide_min_mass,
                peptide_max_mass,
                peptide_type,
                score_backlog
            )
            testers.append(tester)
        self.testers = testers
        self.peptide_type = peptide_type
        self.aa_mass_table = aa_mass_table
        self.aa_mass_tolerance = aa_mass_tolerance

    def test(
            self,
            peptide: List[AA],
            theo_spec: Optional[List[Tuple[float, float, float]]] = None
    ) -> List[TestResult]:
        if theo_spec is None:
            theo_spec = SequenceTester.generate_theroetical_spectrum_with_tolerances(
                peptide,
                self.peptide_type,
                self.aa_mass_table,
                self.aa_mass_tolerance
            )
        return [t.test(peptide, theo_spec) for t in self.testers]


if __name__ == '__main__':
    exp_spec = [0.0, 112.5, 126.8, 163.6, 245.9, 287.0, 400.0]
    peptide_mass_tolerance = experimental_spectrum_peptide_mass_noise(1.0, 3)
    peptide_mass_range_candidates = [(m - peptide_mass_tolerance, m + peptide_mass_tolerance) for m in exp_spec[-3:]]
    aa_masses = spectrum_convolution(exp_spec, 2.0)
    aa_mass_table = {round(k, 0): round(k, 0) for k, v in aa_masses.items()}
    aa_mass_tolerance = 2.0
    seq_tester = SequenceTester(exp_spec, aa_mass_table, aa_mass_tolerance, 390.0, 415.0, PeptideType.LINEAR)
    print(f'{seq_tester.test([112.0, 127.0, 164.0])}')
    print(f'{seq_tester.test([112.0, 164.0, 127.0])}')
    print(f'{seq_tester.test([113.0, 127.0, 164.0])}')
    print(f'{seq_tester.test([113.0, 164.0, 127.0])}')
    print(f'{seq_tester.test([127.0, 164.0, 112.0])}')
    print(f'{seq_tester.test([127.0, 164.0, 113.0])}')
    print(f'{seq_tester.test([164.0, 127.0, 112.0])}')
    print(f'{seq_tester.test([164.0, 127.0, 113.0])}')
