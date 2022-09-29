`{bm-disable-all}`[gt_ch1_code/ReducedFormOrdinalGame.py](gt_ch1_code/ReducedFormOrdinalGame.py) (lines 71 to 75):`{bm-enable-all}`

```python
def strictly_dominates_overall(self, player: int, strategy: str) -> bool:
    for other_strategy in self.strategies[player]:
        if not self.strictly_dominates_other(player, strategy, other_strategy):
            return False
    return True
```