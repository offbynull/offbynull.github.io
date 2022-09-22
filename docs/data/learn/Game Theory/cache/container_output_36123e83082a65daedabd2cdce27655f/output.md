`{bm-disable-all}`[gt_ch1_code/ReducedFormOrdinalGame.py](gt_ch1_code/ReducedFormOrdinalGame.py) (lines 26 to 72):`{bm-enable-all}`

```python
def is_strictly_dominant(self, player: int, strategy1: str, strategy2: str) -> bool:
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
# MARKDOWN_STRICT_DOMINANCE

# MARKDOWN_WEAK_DOMINANCE
def is_weakly_dominant(self, player: int, strategy1: str, strategy2: str) -> bool:
    strict_found = False
    for player_strategy_profile in product(*(s if i != player else {'FAKE'} for i, s in enumerate(self.strategies))):
        player_strategy_profile_1 = list(player_strategy_profile)
        player_strategy_profile_2 = list(player_strategy_profile)
        player_strategy_profile_1[player] = strategy1
        player_strategy_profile_2[player] = strategy2
        payoff_1 = self.player_strategy_profile_preference(player, tuple(player_strategy_profile_1))
        payoff_2 = self.player_strategy_profile_preference(player, tuple(player_strategy_profile_2))
        if not (payoff_1 >= payoff_2):
            return False
        if payoff_1 > payoff_2:
            strict_found = True
    return strict_found
# MARKDOWN_WEAK_DOMINANCE

# MARKDOWN_STRICT_DOMINANCE_TOTAL
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