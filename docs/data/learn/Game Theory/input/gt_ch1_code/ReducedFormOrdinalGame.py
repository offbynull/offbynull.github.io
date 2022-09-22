from abc import ABC, abstractmethod
from itertools import product
from typing import Generator

from GameFrame import GameFrame, MappedOutcomesGameFrame


class ReducedFormOrdinalGame(ABC):
    def __init__(
            self,
            players: list[str],
            strategies: list[set[str]]
    ):
        self.players = players
        self.strategies = strategies

    def strategy_profiles(self) -> Generator[list[str], None, None]:
        for sp in product(*tuple(self.strategies[i] for i in range(len(self.players)))):
            yield list(sp)

    @abstractmethod
    def player_strategy_profile_preference(self, player: int, strategy_profile: tuple[str, ...]) -> int:
        ...

    # MARKDOWN_STRICT_DOMINANCE
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
    # MARKDOWN_STRICT_DOMINANCE_TOTAL

class MappedPreferencesOrdinalGame(ReducedFormOrdinalGame):
    def __init__(
            self,
            players: list[str],
            strategies: list[set[str]],
            player_preference_rankings: dict[int, dict[tuple[str, ...], int]]  # player num -> (strat profile -> preference)
    ):
        super().__init__(players, strategies)
        self.player_preference_rankings = player_preference_rankings

    def player_strategy_profile_preference(self, player: int, strategy_profile: tuple[str, ...]) -> int:
        return self.player_preference_rankings[player][strategy_profile]


if __name__ == '__main__':
    og = MappedPreferencesOrdinalGame(
        ['Alice', 'Bob'],
        [
            {'Lie', 'Get Violent', 'Stay Silent'},
            {'Truth', 'Lie'}
        ],
        {
            0: {
                ('Lie', 'Truth'): 4,
                ('Lie', 'Lie'): 3,
                ('Get Violent', 'Truth'): 2,
                ('Get Violent', 'Lie'): 2,
                ('Stay Silent', 'Truth'): 4,
                ('Stay Silent', 'Lie'): 2.5
            },
            1: {
                ('Lie', 'Truth'): 1,
                ('Lie', 'Lie'): 10,
                ('Get Violent', 'Truth'): 3,
                ('Get Violent', 'Lie'): 6,
                ('Stay Silent', 'Truth'): 1,
                ('Stay Silent', 'Lie'): 10
            }
        }
    )
    print(f'{og.strict_dominance(0)}')
    print(f'{og.strict_dominance(1)}')
    # print(f'{og.is_weakly_dominant(0, "Get Violent", "Lie")}')
    # print(f'{og.is_weakly_dominant(0, "Get Violent", "Stay Silent")}')
    # print(f'{og.is_weakly_dominant(0, "Lie", "Stay Silent")}')
    # m = {(p, tuple(sp)): og.player_strategy_profile_preference(p, tuple(sp)) for (p, _), sp in product(enumerate(og.players), og.strategy_profiles())}
    # print(f'{m}')