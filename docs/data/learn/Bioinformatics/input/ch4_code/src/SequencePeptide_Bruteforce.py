from typing import List, Dict, TypeVar, Tuple

from ExperimentalSpectrumPeptideMassNoise import experimental_spectrum_peptide_mass_noise
from SequenceTester import TestResult, SequenceTesterSet
from SpectrumConvolution import spectrum_convolution
from TheoreticalSpectrum_PrefixSum import PeptideType

AA = TypeVar('AA')


# MARKDOWN
def sequence_peptide(
        exp_spec: List[float],                               # must be sorted asc
        aa_mass_table: Dict[AA, float],                      # amino acid mass table
        aa_mass_tolerance: float,                            # amino acid mass tolerance
        peptide_mass_candidates: List[Tuple[float, float]],  # mass range candidates for mass of peptide
        peptide_type: PeptideType,                           # linear or cyclic
        score_backlog: int = 0                               # backlog of top scores
) -> SequenceTesterSet:
    tester_set = SequenceTesterSet(
        exp_spec,
        aa_mass_table,
        aa_mass_tolerance,
        peptide_mass_candidates,
        peptide_type,
        score_backlog
    )
    candidates = [[]]
    while len(candidates) > 0:
        new_candidate_peptides = []
        for p in candidates:
            for m in aa_mass_table.keys():
                new_p = p[:]
                new_p.append(m)
                res = set(tester_set.test(new_p))
                if res != {TestResult.MASS_TOO_LARGE}:
                    new_candidate_peptides.append(new_p)
        candidates = new_candidate_peptides
    return tester_set
# MARKDOWN


if __name__ == '__main__':
    exp_spec = [0.0, 112.5, 126.8, 163.6, 245.9, 287.0, 400.0]
    aa_masses = spectrum_convolution(exp_spec, 2.0)
    aa_mass_table = {round(k, 0): round(k, 0) for k, v in aa_masses.items()}
    peptide_mass_noise = experimental_spectrum_peptide_mass_noise(1, 3)
    peptide_mass_range_candidates = [(m - peptide_mass_noise, m + peptide_mass_noise)for m in exp_spec[-1:]]
    testers = sequence_peptide(exp_spec, aa_mass_table, 2.0, peptide_mass_range_candidates, PeptideType.LINEAR)
    for tester in testers.testers:
        print(f'For peptides between {tester.peptide_min_mass} and {tester.peptide_max_mass}')
        print(f'-------------------')
        for score, peptides in tester.leader_peptides.items():
            for peptide in peptides:
                print(f'{score}: {peptide}')
