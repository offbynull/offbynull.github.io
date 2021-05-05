`{bm-disable-all}`[ch4_code/src/SequencePeptide_Naive_Bruteforce.py](ch4_code/src/SequencePeptide_Naive_Bruteforce.py) (lines 10 to 30):`{bm-enable-all}`

```python
def sequence_peptide(
        exp_spec: List[float],  # must be sorted asc
        peptide_type: PeptideType,
        aa_mass_table: Dict[AA, float]
) -> List[List[AA]]:
    peptide_mass = exp_spec[-1]
    candidate_peptides = [[]]
    final_peptides = []
    while len(candidate_peptides) > 0:
        new_candidate_peptides = []
        for p in candidate_peptides:
            for m in aa_mass_table.keys():
                new_p = p[:] + [m]
                new_p_mass = sum([aa_mass_table[aa] for aa in new_p])
                if new_p_mass == peptide_mass and theoretical_spectrum(new_p, peptide_type, aa_mass_table) == exp_spec:
                    final_peptides.append(new_p)
                elif new_p_mass < peptide_mass:
                    new_candidate_peptides.append(new_p)
        candidate_peptides = new_candidate_peptides
    return final_peptides
```