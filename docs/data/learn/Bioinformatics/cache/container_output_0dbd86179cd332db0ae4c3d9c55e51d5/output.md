`{bm-disable-all}`[ch4_code/src/SpectrumScore_NoNoise.py](ch4_code/src/SpectrumScore_NoNoise.py) (lines 9 to 28):`{bm-enable-all}`

```python
def score_spectrums(
        s1: List[float],  # must be sorted ascending
        s2: List[float]   # must be sorted ascending
) -> int:
    idx_s1 = 0
    idx_s2 = 0
    score = 0
    while idx_s1 < len(s1) and idx_s2 < len(s2):
        s1_mass = s1[idx_s1]
        s2_mass = s2[idx_s2]
        if s1_mass < s2_mass:
            idx_s1 += 1
        elif s1_mass > s2_mass:
            idx_s2 += 1
        else:
            idx_s1 += 1
            idx_s2 += 1
            score += 1
    return score
```