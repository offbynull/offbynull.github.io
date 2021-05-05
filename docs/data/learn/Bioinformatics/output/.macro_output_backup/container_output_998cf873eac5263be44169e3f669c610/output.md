`{bm-disable-all}`[ch4_code/src/TheoreticalSpectrum_Bruteforce.py](ch4_code/src/TheoreticalSpectrum_Bruteforce.py) (lines 10 to 26):`{bm-enable-all}`

```python
def theoretical_spectrum(
        peptide: List[AA],
        peptide_type: PeptideType,
        mass_table: Dict[AA, float]
) -> List[int]:
    # add subpeptide of length 0's mass
    ret = [0.0]
    # add subpeptide of length 1 to k-1's mass
    for k in range(1, len(peptide)):
        for subpeptide, _ in slide_window(peptide, k, cyclic=peptide_type == PeptideType.CYCLIC):
            ret.append(sum([mass_table[ch] for ch in subpeptide]))
    # add subpeptide of length k's mass
    ret.append(sum([mass_table[aa] for aa in peptide]))
    # sort and return
    ret.sort()
    return ret
```