`{bm-disable-all}`[ch4_code/src/SequencePeptide_Leaderboard.py](ch4_code/src/SequencePeptide_Leaderboard.py) (lines 14 to 79):`{bm-enable-all}`

```python
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
```