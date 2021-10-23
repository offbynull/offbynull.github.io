`{bm-disable-all}`[ch4_code/src/SequencePeptide_Bruteforce.py](ch4_code/src/SequencePeptide_Bruteforce.py) (lines 13 to 41):`{bm-enable-all}`

```python
def sequence_peptide(
        exp_spec: List[float],                               # must be sorted asc
        aa_mass_table: Dict[AA, float],                      # amino acid mass table
        aa_mass_tolerance: float,                            # amino acid mass tolerance
        peptide_mass_candidates: List[Tuple[float, float]],  # mass range candidates for mass of peptide
        peptide_type: PeptideType,                           # linear or cyclic
        score_backlog: int                                   # backlog of top scores
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
```