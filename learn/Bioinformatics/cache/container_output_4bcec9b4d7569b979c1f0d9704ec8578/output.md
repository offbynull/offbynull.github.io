`{bm-disable-all}`[ch4_code/src/TheoreticalSpectrumTolerances.py](ch4_code/src/TheoreticalSpectrumTolerances.py) (lines 7 to 26):`{bm-enable-all}`

```python
def theoretical_spectrum_tolerances(
        peptide_len: int,
        peptide_type: PeptideType,
        amino_acid_mass_tolerance: float
) -> List[float]:
    ret = [0.0]
    if peptide_type == PeptideType.LINEAR:
        for i in range(peptide_len):
            tolerance = (i + 1) * amino_acid_mass_tolerance
            ret += [tolerance] * (peptide_len - i)
    elif peptide_type == PeptideType.CYCLIC:
        for i in range(peptide_len - 1):
            tolerance = (i + 1) * amino_acid_mass_tolerance
            ret += [tolerance] * peptide_len
        if peptide_len != 0:
            ret.append(peptide_len * amino_acid_mass_tolerance)
    else:
        raise ValueError()
    return ret
```