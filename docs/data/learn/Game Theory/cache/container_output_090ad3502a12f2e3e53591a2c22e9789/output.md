`{bm-disable-all}`[gt_ch1_code/ReducedFormOrdinalGame.py](gt_ch1_code/ReducedFormOrdinalGame.py) (lines 92 to 95):`{bm-enable-all}`

```python
def strictly_dominant_strategy_equilibrium(self, strategy_profile: list[str]):
    for i, _ in enumerate(self.players):
        if not self.strictly_dominates_overall(i, strategy_profile[i]):
            return False
    return True
```