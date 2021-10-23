`{bm-disable-all}`[ch4_code/src/SequencePeptide_BranchAndBound.py](ch4_code/src/SequencePeptide_BranchAndBound.py) (lines 14 to 78):`{bm-enable-all}`

```python
def sequence_peptide(
        exp_spec: List[float],                               # must be sorted asc
        aa_mass_table: Dict[AA, float],                      # amino acid mass table
        aa_mass_tolerance: float,                            # amino acid mass tolerance
        peptide_mass_candidates: List[Tuple[float, float]],  # mass range candidates for mass of peptide
        peptide_type: PeptideType,                           # linear or cyclic
        score_backlog: int,                                  # backlog of top scores
        candidate_threshold: float                           # if < 1 then min % match, else min count match
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
            if {TestResult.MASS_TOO_LARGE} == res:
                removal_idxes.add(i)
            else:
                # Why get the theo spec of the linear version even if the peptide is cyclic? Think about what's
                # happening here. If the exp spec is for cyclic peptide NQYQ, and you're checking to see if the
                # candidate NQY should continue to be branched out...
                #
                # Exp spec  cyclic NQYQ: [0, 114, 128, 128, 163, 242, 242,      291, 291, 370, 405, 405, 419, 533]
                # Theo spec cyclic NQY:  [0, 114, 128,      163, 242,      277, 291,           405]
                #                                                           ^
                #                                                           |
                #                                                        mass(YN)
                #
                # Since NQY is being treated as a cyclic peptide, it has the subpeptide YN (mass of 277). However, the
                # cyclic peptide NQYQ doesn't have the subpeptide YN. That means NQY won't be branched out any further
                # even though it should. As such, even if the exp spec is for a cyclic peptide, treat the candidates as
                # linear segments of that cyclic peptide (essentially linear peptides).
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
```