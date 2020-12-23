from typing import List, Dict, TypeVar, Optional

from SpectrumScore_NoNoise import score_spectrums
from TheoreticalSpectrum_PrefixSum import theoretical_spectrum, PeptideType
from helpers.AminoAcidUtils import get_amino_acid_to_mass_table

AA = TypeVar('AA')


# MARKDOWN
def sequence_peptide(
        exp_spec: List[float],  # must be sorted
        peptide_type: PeptideType,
        peptide_mass: Optional[float],
        aa_mass_table: Dict[AA, float],
        leaderboard_size: int
) -> List[List[AA]]:
    # Exp_spec could be missing masses / have faulty masses, but even so assume the last mass in exp_spec is the peptide
    # mass if the user didn't supply one. This may not be correct -- it's a best guess.
    if peptide_mass is None:
        peptide_mass = exp_spec[-1]
    leaderboard = [[]]
    final_peptides = [next(iter(leaderboard))]
    final_score = score_spectrums(
        theoretical_spectrum(final_peptides[0], PeptideType.CYCLIC, aa_mass_table),
        exp_spec
    )
    while len(leaderboard) > 0:
        # Branch leaderboard
        expanded_leaderboard = []
        for p in leaderboard:
            for m in aa_mass_table:
                new_p = p[:] + [m]
                expanded_leaderboard.append(new_p)
        # Pull out any expanded_leaderboard peptides with mass >= peptide_mass
        removal_idxes = set()
        for i, p in enumerate(expanded_leaderboard):
            p_mass = sum([aa_mass_table[aa] for aa in p])
            if p_mass == peptide_mass:
                # The peptide's mass is equal to the expected mass. Check if the score against the current top score. If
                # it's ...
                #  * the same score, remove it and add it as a final peptide.
                #  * a higher score, remove it and reset the final peptides to this.
                #  * a lower score, remove and discard it.
                theo_spec = theoretical_spectrum(p, peptide_type, aa_mass_table)
                score = score_spectrums(theo_spec, exp_spec)
                if score > final_score:
                    final_peptides = [p]
                    final_score = score_spectrums(
                        theoretical_spectrum(final_peptides[0], peptide_type, aa_mass_table),
                        exp_spec
                    )
                elif score == final_score:
                    final_peptides.append(p)
                removal_idxes.add(i)
            elif p_mass > peptide_mass:
                # The peptide's mass exceeds the expected mass, meaning that there's no chance that this peptide can be
                # a match for exp_spec. Discard it.
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
        theo_specs = [theoretical_spectrum(p, PeptideType.LINEAR, aa_mass_table) for p in expanded_leaderboard]
        scores = [score_spectrums(theo_spec, exp_spec) for theo_spec in theo_specs]
        score_pairs = sorted(zip(expanded_leaderboard, scores), key=lambda x: x[1], reverse=True)
        trim_pos = leaderboard_size
        tail_score = 0 if len(score_pairs) == 0 else score_pairs[-1][1]
        for j in range(leaderboard_size + 1, len(score_pairs)):
            if score_pairs[j][1] < tail_score:
                trim_pos = j
                break
        leaderboard = [p for p, _ in score_pairs[:trim_pos]]
    return final_peptides
# MARKDOWN


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        exp_spec = [float(m) for m in input().strip().split()]
        peptide_type = input().strip()
        peptide_mass = float(input().strip())
        leaderboard_size = int(input().strip())
        mass_table = {e.strip().split(':')[0]: float(e.strip().split(':')[1]) for e in input().strip().split(',')}
        peptides = sequence_peptide(
            exp_spec,
            {'cyclic': PeptideType.CYCLIC, 'linear': PeptideType.LINEAR}[peptide_type],
            peptide_mass,
            mass_table,
            leaderboard_size
        )
        print(f'The {peptide_type} peptides matching the experimental spectrum {exp_spec} are with leaderboard size'
              f' of {leaderboard_size}...', end="\n\n")
        for peptide in peptides:
            print(f' * {"".join(peptide)}')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()
