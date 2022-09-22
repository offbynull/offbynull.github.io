`{bm-disable-all}`[gt_ch1_code/ReducedFormOrdinalGame.py](gt_ch1_code/ReducedFormOrdinalGame.py) (lines 57 to 72):`{bm-enable-all}`

```python
def strict_dominance(self, player: int) -> str | None:
    strategy_to_payoffs = []
    for strategy in self.strategies[player]:
        strategy_payoffs = []
        for player_strategy_profile in product(*(s if i != player else {'FAKE'} for i, s in enumerate(self.strategies))):
            _player_strategy_profile = list(player_strategy_profile)
            _player_strategy_profile[player] = strategy
            payoff = self.player_strategy_profile_preference(player, tuple(_player_strategy_profile))
            strategy_payoffs.append(payoff)
        strategy_to_payoffs.append([strategy, strategy_payoffs])
    strategy_to_payoffs.sort(key=lambda x: x[1])
    top_strategy, top_payoffs = strategy_to_payoffs.pop()
    next_strategy, next_payoffs = strategy_to_payoffs.pop() if strategy_to_payoffs != [] else (None, [])
    if top_payoffs > next_payoffs:
        return top_strategy
    return None
```