`{bm-disable-all}`[gt_ch1_code/ReducedFormOrdinalGame.py](gt_ch1_code/ReducedFormOrdinalGame.py) (lines 79 to 84):`{bm-enable-all}`

```python
def weakly_dominates_overall(self, player: int, strategy: str) -> bool:
    for other_strategy in self.strategies[player]:
        if not self.weakly_dominates_other(player, strategy, other_strategy) \
                and not self.equivalent_to_other(player, strategy, other_strategy):
            return False
    return True
```