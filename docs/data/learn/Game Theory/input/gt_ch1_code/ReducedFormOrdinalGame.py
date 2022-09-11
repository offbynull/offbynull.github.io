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
    def player_strategy_profile_preference(self, player: int, outcome: str) -> int:
        ...


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
            {'Split', 'Steal'},
            {'Split', 'Steal'}
        ],
        {
            0: {
                ('Split', 'Split'): 1,
                ('Split', 'Steal'): 0,
                ('Steal', 'Split'): 2,
                ('Steal', 'Steal'): 0
            },
            1: {
                ('Split', 'Split'): 1,
                ('Split', 'Steal'): 2,
                ('Steal', 'Split'): 0,
                ('Steal', 'Steal'): 0
            }
        }
    )

    m = {(p, tuple(sp)): og.player_strategy_profile_preference(p, tuple(sp)) for (p, _), sp in product(enumerate(og.players), og.strategy_profiles())}
    print(f'{m}')