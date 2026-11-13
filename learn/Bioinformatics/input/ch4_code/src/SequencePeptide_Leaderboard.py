from typing import List, Dict, TypeVar, Tuple

from ExperimentalSpectrumPeptideMassNoise import experimental_spectrum_peptide_mass_noise
from PeptideType import PeptideType
from SequenceTester import TestResult, SequenceTesterSet, SequenceTester
from SpectrumConvolution import spectrum_convolution
from SpectrumConvolutionNoise import spectrum_convolution_noise
from SpectrumScore import score_spectrums

AA = TypeVar('AA')


# MARKDOWN
def sequence_peptide(
        exp_spec: List[float],                               # must be sorted asc
        aa_mass_table: Dict[AA, float],                      # amino acid mass table
        aa_mass_tolerance: float,                            # amino acid mass tolerance
        peptide_mass_candidates: List[Tuple[float, float]],  # mass range candidates for mass of peptide
        peptide_type: PeptideType,                           # linear or cyclic
        score_backlog: int,                                  # backlog of top scores
        leaderboard_size: int,
        leaderboard_initial: List[List[AA]] = None           # bootstrap candidate peptides for leaderboard
) -> SequenceTesterSet:
    tester_set = SequenceTesterSet(
        exp_spec,
        aa_mass_table,
        aa_mass_tolerance,
        peptide_mass_candidates,
        peptide_type,
        score_backlog
    )
    if leaderboard_initial is None:
        leaderboard = [[]]
    else:
        leaderboard = leaderboard_initial[:]
    while len(leaderboard) > 0:
        # Branch candidates
        expanded_leaderboard = []
        for p in leaderboard:
            for m in aa_mass_table:
                new_p = p[:] + [m]
                expanded_leaderboard.append(new_p)
        # Test candidates to see if they match exp_spec or if they should keep being branched
        removal_idxes = set()
        for i, p in enumerate(expanded_leaderboard):
            res = set(tester_set.test(p))
            if {TestResult.MASS_TOO_LARGE} == res:
                removal_idxes.add(i)
        expanded_leaderboard = [p for i, p in enumerate(expanded_leaderboard) if i not in removal_idxes]
        # Set leaderboard to the top n scoring peptides from expanded_leaderboard, but include peptides past n as long
        # as those peptides have a score equal to the nth peptide. The reason for this is that because they score the
        # same, there's just as much of a chance that they'll end up as the winner as it is that the nth peptide will.
            # NOTE: Why get the theo spec of the linear version even if the peptide is cyclic? For similar reasons as to
            # why it's done in the branch-and-bound variant: If we treat candidate peptides as cyclic, their theo spec
            # will include masses for wrapping subpeptides of the candidate peptide. These wrapping subpeptide masses
            # may end up inadvertently matching masses in the experimental spectrum, meaning that the candidate may get
            # a better score than it should, potentially pushing it forward over other candidates that would ultimately
            # branch out  to a more optimal final solution. As such, even if the exp  spec is  for a cyclic peptide,
            # treat the candidates as linear segments of that cyclic peptide (essentially linear  peptides).
        theo_specs = [
            SequenceTester.generate_theroetical_spectrum_with_tolerances(
                p,
                peptide_type,
                aa_mass_table,
                aa_mass_tolerance
            )
            for p in expanded_leaderboard
        ]
        scores = [score_spectrums(exp_spec, theo_spec) for theo_spec in theo_specs]
        scores_paired = sorted(zip(expanded_leaderboard, scores), key=lambda x: x[1], reverse=True)
        leaderboard_tail_idx = min(leaderboard_size, len(scores_paired)) - 1
        leaderboard_tail_score = 0 if leaderboard_tail_idx == -1 else scores_paired[leaderboard_tail_idx][1]
        for j in range(leaderboard_tail_idx + 1, len(scores_paired)):
            if scores_paired[j][1] < leaderboard_tail_score:
                leaderboard_tail_idx = j - 1
                break
        leaderboard = [p for p, _ in scores_paired[:leaderboard_tail_idx + 1]]
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
        aa_top_n = int(input().strip())
        aa_masses = spectrum_convolution(exp_spec, aa_mass_noise)
        aa_mass_table = {round(k, aa_mass_round): round(k, aa_mass_round) for k, v in aa_masses.most_common(aa_top_n)}
        peptide_type = input().strip()
        peptide_expected_len = int(input().strip())
        peptide_mass_noise = experimental_spectrum_peptide_mass_noise(exp_spec_mass_noise, peptide_expected_len)
        peptide_mass_range_candidates = [(m - peptide_mass_noise, m + peptide_mass_noise) for m in exp_spec[-exp_spec_final_mass_in_last_n:]]
        score_backlog = int(input().strip())
        leaderboard_size = int(input().strip())
        testers = sequence_peptide(
            exp_spec,
            aa_mass_table,
            aa_mass_noise,
            peptide_mass_range_candidates,
            {'cyclic': PeptideType.CYCLIC, 'linear': PeptideType.LINEAR}[peptide_type],
            score_backlog,
            leaderboard_size
        )
        print(f'Given the ...', end='\n\n')
        print(f' * experimental spectrum: {exp_spec}')
        print(f' * experimental spectrum mass noise: ±{exp_spec_mass_noise}')
        print(f' * assumed peptide type: {peptide_type}')
        print(f' * assumed peptide length: {peptide_expected_len}')
        print(f' * assumed peptide mass: any of the last {exp_spec_final_mass_in_last_n} experimental spectrum masses')
        print(f' * score backlog: {score_backlog}')
        print(f' * leaderboard size: {leaderboard_size}', end='\n\n')
        print(f'Top {aa_top_n} captured mino acid masses (rounded to {aa_mass_round}): {list(aa_mass_table.keys())}',
              end='\n\n')
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
