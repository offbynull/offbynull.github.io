from typing import List, Dict, TypeVar, Tuple

from ExperimentalSpectrumPeptideMassNoise import experimental_spectrum_peptide_mass_noise
from SequenceTester import SequenceTester, TestResult
from SpectrumConvolution import spectrum_convolution
from TheoreticalSpectrum_PrefixSum import PeptideType

AA = TypeVar('AA')


def sequence_peptide(
        exp_spec: List[float],                               # must be sorted asc
        aa_mass_table: Dict[AA, float],                      # amino acid mass table
        aa_mass_tolerance: float,                            # amino acid mass tolerance
        peptide_mass_candidates: List[Tuple[float, float]],  # mass range candidates for mass of peptide
        peptide_type: PeptideType                            # linear or cyclic
) -> List[SequenceTester]:
    testers = []
    for min_mass, max_mass in peptide_mass_candidates:
        tester = SequenceTester(exp_spec, aa_mass_table, aa_mass_tolerance, min_mass, max_mass, peptide_type)
        testers.append(tester)
    candidates = [[]]
    while len(candidates) > 0:
        new_candidate_peptides = []
        for p in candidates:
            for m in aa_mass_table.keys():
                new_p = p[:]
                new_p.append(m)
                res = {tester.test(new_p) for tester in testers}
                if res != {TestResult.MASS_TOO_LARGE}:
                    new_candidate_peptides.append(new_p)
        candidates = new_candidate_peptides
    return testers


if __name__ == '__main__':
    exp_spec = [0.0, 112.5, 126.8, 163.6, 245.9, 287.0, 400.0]
    aa_masses = spectrum_convolution(exp_spec, 2.0)
    aa_mass_table = {round(k, 0): round(k, 0) for k, v in aa_masses.items()}
    peptide_mass_noise = experimental_spectrum_peptide_mass_noise(1, 3)
    peptide_mass_range = exp_spec[-1] - peptide_mass_noise, exp_spec[-1] + peptide_mass_noise
    testers = sequence_peptide(exp_spec, aa_mass_table, 2.0, [peptide_mass_range], PeptideType.LINEAR)
    for tester in testers:
        print(f'For peptides between {tester.peptide_min_mass} and {tester.peptide_max_mass}')
        print(f'-------------------')
        for score, peptides in tester.leader_peptides.items():
            for peptide in peptides:
                print(f'{score}: {peptide}')
