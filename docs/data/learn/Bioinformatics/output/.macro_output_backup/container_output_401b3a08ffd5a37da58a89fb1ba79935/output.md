`{bm-disable-all}`[ch4_code/src/ExperimentalSpectrum.py](ch4_code/src/ExperimentalSpectrum.py) (lines 6 to 14):`{bm-enable-all}`

```python
# Its expected that low intensity mass_charge_ratios have already been filtered out prior to invoking this func.
def experimental_spectrum(mass_charge_ratios: List[float], charge_tendencies: Set[float]) -> List[float]:
    ret = [0.0]  # implied -- subpeptide of length 0
    for mcr in mass_charge_ratios:
        for charge in charge_tendencies:
            ret.append(mcr * charge)
    ret.sort()
    return ret
```