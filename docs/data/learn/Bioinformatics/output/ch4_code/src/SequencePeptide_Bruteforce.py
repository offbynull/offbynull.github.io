from typing import List, Dict, TypeVar, Tuple

from ExperimentalSpectrumPeptideMassNoise import experimental_spectrum_peptide_mass_noise
from SequenceTester import TestResult, SequenceTesterSet
from SpectrumConvolution import spectrum_convolution
from SpectrumConvolutionNoise import spectrum_convolution_noise
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


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        exp_spec = [float(m) for m in input().strip().split()]
        exp_spec_mass_noise = float(input().strip())
        exp_spec_final_mass_in_last_n = int(input().strip())
        aa_mass_noise = spectrum_convolution_noise(exp_spec_mass_noise)
        aa_mass_round = int(input().strip())
        aa_masses = spectrum_convolution(exp_spec, aa_mass_noise)
        aa_mass_table = {round(k, aa_mass_round): round(k, aa_mass_round) for k, v in aa_masses.items()}
        peptide_type = input().strip()
        peptide_expected_len = int(input().strip())
        peptide_mass_noise = experimental_spectrum_peptide_mass_noise(exp_spec_mass_noise, peptide_expected_len)
        peptide_mass_range_candidates = [(m - peptide_mass_noise, m + peptide_mass_noise) for m in exp_spec[-exp_spec_final_mass_in_last_n:]]
        score_backlog = int(input().strip())
        testers = sequence_peptide(
            exp_spec,
            aa_mass_table,
            aa_mass_noise,
            peptide_mass_range_candidates,
            {'cyclic': PeptideType.CYCLIC, 'linear': PeptideType.LINEAR}[peptide_type],
            score_backlog
        )
        print(f'Given the ...', end='\n\n')
        print(f' * experimental spectrum: {exp_spec}')
        print(f' * experimental spectrum mass noise: ±{exp_spec_mass_noise}')
        print(f' * assumed peptide type: {peptide_type}')
        print(f' * assumed peptide length: {peptide_expected_len}')
        print(f' * assumed peptide mass: any of the last {exp_spec_final_mass_in_last_n} experimental spectrum masses')
        print(f' * score backlog: {score_backlog}', end='\n\n')
        print(f'Captured mino acid masses are (rounded to {aa_mass_round}): {list(aa_mass_table.keys())}', end='\n\n')
        for tester in testers.testers:
            print(f'For peptides between {tester.peptide_min_mass} and {tester.peptide_max_mass}...', end='\n\n')
            for score, peptides in tester.leader_peptides.items():
                for peptide in peptides:
                    print(f' * Score {score}: {"-".join([str(aa) for aa in peptide])}')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()


# if __name__ == '__main__':
#     exp_spec = [0.0, 112.5, 126.8, 163.6, 245.9, 287.0, 400.0]
#     aa_masses = spectrum_convolution(exp_spec, 2.0)
#     aa_mass_table = {round(k, 0): round(k, 0) for k, v in aa_masses.items()}
#     peptide_mass_noise = experimental_spectrum_peptide_mass_noise(1, 3)
#     peptide_mass_range_candidates = [(m - peptide_mass_noise, m + peptide_mass_noise)for m in exp_spec[-1:]]
#     testers = sequence_peptide(exp_spec, aa_mass_table, 2.0, peptide_mass_range_candidates, PeptideType.LINEAR)
#     for tester in testers.testers:
#         print(f'For peptides between {tester.peptide_min_mass} and {tester.peptide_max_mass}')
#         print(f'-------------------')
#         for score, peptides in tester.leader_peptides.items():
#             for peptide in peptides:
#                 print(f'{score}: {peptide}')
