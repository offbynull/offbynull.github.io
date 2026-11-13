`{bm-disable-all}`[gt_ch1_code/ReducedFormOrdinalGame.py](gt_ch1_code/ReducedFormOrdinalGame.py) (lines 26 to 36):`{bm-enable-all}`

```python
def strictly_dominates_other(self, player: int, strategy1: str, strategy2: str) -> bool:
    for player_strategy_profile in product(*(s if i != player else {'FAKE'} for i, s in enumerate(self.strategies))):
        player_strategy_profile_1 = list(player_strategy_profile)
        player_strategy_profile_2 = list(player_strategy_profile)
        player_strategy_profile_1[player] = strategy1
        player_strategy_profile_2[player] = strategy2
        payoff_1 = self.player_strategy_profile_preference(player, tuple(player_strategy_profile_1))
        payoff_2 = self.player_strategy_profile_preference(player, tuple(player_strategy_profile_2))
        if not (payoff_1 > payoff_2):
            return False
    return True
```