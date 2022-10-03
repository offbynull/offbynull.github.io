`{bm-disable-all}`[gt_ch1_code/ReducedFormOrdinalGame.py](gt_ch1_code/ReducedFormOrdinalGame.py) (lines 100 to 106):`{bm-enable-all}`

```python
def weakly_dominant_strategy_equilibrium(self, strategy_profile: list[str]):
    found_strict_dom = False
    for i, _ in enumerate(self.players):
        if not self.weakly_dominates_overall(i, strategy_profile[i]):
            return False
        found_strict_dom = self.strictly_dominates_overall(i, strategy_profile[i])
    return found_strict_dom
```