`{bm-disable-all}`[ch4_code/src/SpectrumConvolution_NoNoise.py](ch4_code/src/SpectrumConvolution_NoNoise.py) (lines 6 to 16):`{bm-enable-all}`

```python
def spectrum_convolution(experimental_spectrum: List[float], min_mass=57.0, max_mass=200.0) -> List[float]:
    # it's expected that experimental_spectrum is sorted smallest to largest
    diffs = []
    for row_idx, row_mass in enumerate(experimental_spectrum):
        for col_idx, col_mass in enumerate(experimental_spectrum):
            mass_diff = row_mass - col_mass
            if min_mass <= mass_diff <= max_mass:
                diffs.append(mass_diff)
    diffs.sort()
    return diffs
```