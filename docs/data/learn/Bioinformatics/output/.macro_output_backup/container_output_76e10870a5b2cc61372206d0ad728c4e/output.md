`{bm-disable-all}`[ch4_code/src/ExperimentalSpectrumNoise.py](ch4_code/src/ExperimentalSpectrumNoise.py) (lines 6 to 8):`{bm-enable-all}`

```python
def experimental_spectrum_noise(max_mass_charge_ratio_noise: float, charge_tendencies: Set[float]) -> float:
    return max_mass_charge_ratio_noise * abs(max(charge_tendencies))
```