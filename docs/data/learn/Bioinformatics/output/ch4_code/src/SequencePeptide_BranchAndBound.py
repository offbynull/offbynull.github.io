from typing import List, Dict, TypeVar, Tuple

from ExperimentalSpectrumPeptideMassNoise import experimental_spectrum_peptide_mass_noise
from SequenceTester import TestResult, SequenceTesterSet, SequenceTester
from SpectrumConvolution import spectrum_convolution
from SpectrumConvolutionNoise import spectrum_convolution_noise
from SpectrumScore import score_spectrums
from TheoreticalSpectrum_PrefixSum import PeptideType, theoretical_spectrum

AA = TypeVar('AA')


# MARKDOWN
def sequence_peptide(
        exp_spec: List[float],                               # must be sorted asc
        aa_mass_table: Dict[AA, float],                      # amino acid mass table
        aa_mass_tolerance: float,                            # amino acid mass tolerance
        peptide_mass_candidates: List[Tuple[float, float]],  # mass range candidates for mass of peptide
        peptide_type: PeptideType,                           # linear or cyclic
        score_backlog: int = 0,                              # backlog of top scores
        candidate_threshold: float = 0.5                     # if < 1 then min % match, else min count match
) -> SequenceTesterSet:
    tester_set = SequenceTesterSet(
        exp_spec,
        aa_mass_table,
        aa_mass_tolerance,
        peptide_mass_candidates,
        peptide_type,
        score_backlog
    )
    candidate_peptides = [[]]
    while len(candidate_peptides) > 0:
        # Branch candidates
        new_candidate_peptides = []
        for p in candidate_peptides:
            for m in aa_mass_table:
                new_p = p[:] + [m]
                new_candidate_peptides.append(new_p)
        candidate_peptides = new_candidate_peptides
        # Test candidates to see if they match exp_spec or if they should keep being branched
        removal_idxes = set()
        for i, p in enumerate(candidate_peptides):
            res = set(tester_set.test(p))
            if {TestResult.MASS_TOO_LARGE} == res\
                    or {TestResult.ADDED} == res\
                    or {TestResult.MASS_TOO_LARGE, TestResult.ADDED} == res:
                removal_idxes.add(i)
            else:
                # Why get the theo spec of the linear version even if the peptide is cyclic? Think about what's
                # happening here. If the exp spec is for cyclic peptide NQYQ, and you're checking to see if the
                # candidate NQY should continue to be branched out...
                #
                # Exp spec  cyclic NQYQ: [0, 114, 128, 128, 163, 242, 242,      291, 291, 370, 405, 405, 419, 533]
                # Theo spec cyclic NQY:  [0, 114, 128,      163, 242,      277, 291,           405]
                #
                # Given the specs above, the theo spec contains 277 but the exp spec doesn't. That means NQY won't be
                # branched out any further even though it should. As such, even if the exp spec is for a cyclic peptide,
                # treat the candidates as linear segments of that cyclic peptide (essentially linear peptides).
                #
                # Exp spec  cyclic NQYQ: [0, 114, 128, 128, 163, 242, 242, 291, 291, 370, 405, 405, 419, 533]
                # Theo spec linear NQY:  [0, 114, 128,      163, 242,      291,           405]
                #
                # Given the specs above, the exp spec contains all masses in the theo spec.
                theo_spec = SequenceTester.generate_theroetical_spectrum_with_tolerances(
                    p,
                    PeptideType.LINEAR,
                    aa_mass_table,
                    aa_mass_tolerance
                )
                score = score_spectrums(exp_spec, theo_spec)
                if (candidate_threshold < 1.0 and score[0] / len(theo_spec) < candidate_threshold)\
                        or score[0] < candidate_threshold:
                    removal_idxes.add(i)
        candidate_peptides = [p for i, p in enumerate(candidate_peptides) if i not in removal_idxes]
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
        candidate_threshold = float(input().strip())
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
        print(f' * score backlog: {score_backlog}')
        print(f' * candidate threshold: {candidate_threshold * (100.0 if candidate_threshold < 1.0 else 1.0)}'
              f'{"%" if candidate_threshold < 1.0 else ""} mass matches per iteration', end='\n\n')
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
