`{bm-disable-all}`[ch4_code/src/ExperimentalSpectrumPeptideMassNoise.py](ch4_code/src/ExperimentalSpectrumPeptideMassNoise.py) (lines 18 to 21):`{bm-enable-all}`

```python
def experimental_spectrum_peptide_mass_noise(exp_spec_mass_noise: float, peptide_len: int) -> float:
    aa_mass_noise = spectrum_convolution_noise(exp_spec_mass_noise)
    return aa_mass_noise * peptide_len + exp_spec_mass_noise
```