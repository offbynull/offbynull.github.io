`{bm-disable-all}`[ch4_code/src/SequencePeptide_Naive_Leaderboard.py](ch4_code/src/SequencePeptide_Naive_Leaderboard.py) (lines 11 to 95):`{bm-enable-all}`

```python
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
        theoretical_spectrum(final_peptides[0], peptide_type, aa_mass_table),
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
                #  * a higher score, reset the final peptides to it.
                #  * the same score, add it to the final peptides.
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
                # p should be removed at this point (the line below should be uncommented). Not removing it means that
                # it may end up in the leaderboard for the next cycle. If that happens, it'll get branched out into new
                # candidate peptides where each has an amino acids appended.
                #
                # The problem with branching p out further is that p's mass already matches the expected peptide mass.
                # Once p gets branched out, those branched out candidate peptides will have masses that EXCEED the
                # expected peptide mass, meaning they'll all get removed anyway. This would be fine, except that by
                # moving p into the leaderboard for the next cycle you're potentially preventing other viable
                # candidate peptides from making it in.
                #
                # So why isn't p being removed here (why was the line below commented out)? The questions on Stepik
                # expect no removal at this point. Uncommenting it will cause more peptides than are expected to show up
                # for some questions, meaning the answer will be rejected by Stepik.
                #
                # removal_idxes.add(i)
            elif p_mass > peptide_mass:
                # The peptide's mass exceeds the expected mass, meaning that there's no chance that this peptide can be
                # a match for exp_spec. Discard it.
                removal_idxes.add(i)
        expanded_leaderboard = [p for i, p in enumerate(expanded_leaderboard) if i not in removal_idxes]
        # Set leaderboard to the top n scoring peptides from expanded_leaderboard, but include peptides past n as long
        # as those peptides have a score equal to the nth peptide. The reason for this is that because they score the
        # same, there's just as much of a chance that they'll end up as a winner as it is that the nth peptide will.
            # NOTE: Why get the theo spec of the linear version even if the peptide is cyclic? For similar reasons as to
            # why it's done in the branch-and-bound variant: If we treat candidate peptides as cyclic, their theo spec
            # will include masses for wrapping subpeptides of the candidate peptide. These wrapping subpeptide masses
            # may end up inadvertently matching masses in the experimental spectrum, meaning that the candidate may get
            # a better score than it should, potentially pushing it forward over other candidates that would ultimately
            # branch out  to a more optimal final solution. As such, even if the exp  spec is  for a cyclic peptide,
            # treat the candidates as linear segments of that cyclic peptide (essentially linear  peptides). If you're
            # confused go see the comment in the branch-and-bound variant.
        theo_specs = [theoretical_spectrum(p, PeptideType.LINEAR, aa_mass_table) for p in expanded_leaderboard]
        scores = [score_spectrums(theo_spec, exp_spec) for theo_spec in theo_specs]
        scores_paired = sorted(zip(expanded_leaderboard, scores), key=lambda x: x[1], reverse=True)
        leaderboard_trim_to_size = len(expanded_leaderboard)
        for j in range(leaderboard_size + 1, len(scores_paired)):
            if scores_paired[leaderboard_size][1] > scores_paired[j][1]:
                leaderboard_trim_to_size = j - 1
                break
        leaderboard = [p for p, _ in scores_paired[:leaderboard_trim_to_size]]
    return final_peptides
```