`{bm-disable-all}`[ch4_code/src/TheoreticalSpectrum_PrefixSum.py](ch4_code/src/TheoreticalSpectrum_PrefixSum.py) (lines 37 to 53):`{bm-enable-all}`

```python
def theoretical_spectrum(
        peptide: List[AA],
        peptide_type: PeptideType,
        mass_table: Dict[AA, float]
) -> List[float]:
    prefixsum_masses = list(accumulate([mass_table[aa] for aa in peptide], initial=0.0))
    ret = [0.0]
    for end_idx in range(0, len(prefixsum_masses)):
        for start_idx in range(0, end_idx):
            min_mass = prefixsum_masses[start_idx]
            max_mass = prefixsum_masses[end_idx]
            ret.append(max_mass - min_mass)
            if peptide_type == PeptideType.CYCLIC and start_idx > 0 and end_idx < len(peptide):
                ret.append(prefixsum_masses[-1] - (prefixsum_masses[end_idx] - prefixsum_masses[start_idx]))
    ret.sort()
    return ret
```