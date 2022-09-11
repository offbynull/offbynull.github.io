import json
from abc import ABC, abstractmethod
from itertools import product
from typing import Generator


class GameFrame(ABC):
    def __init__(
            self,
            players: list[str],
            strategies: list[set[str]],
            outcomes: set[str]
    ):
        self.players = players
        self.strategies = strategies
        self.outcomes = outcomes

    def strategy_profiles(self) -> Generator[list[str], None, None]:
        for sp in product(*tuple(self.strategies[i] for i in range(len(self.players)))):
            yield list(sp)

    @abstractmethod
    def strategy_profile_to_outcome(self, strategy_profile: list[str]):
        ...


class MappedOutcomesGameFrame(GameFrame):
    def __init__(
            self,
            players: list[str],
            strategies: list[set[str]],
            outcomes: set[str],
            sp_to_outcome: dict[tuple[str, ...], str]
    ):
        super().__init__(players, strategies, outcomes)
        self.sp_to_outcome = sp_to_outcome

    def strategy_profile_to_outcome(self, strategy_profile: list[str]):
        return self.sp_to_outcome[tuple(strategy_profile)]


if __name__ == '__main__':
    gf = MappedOutcomesGameFrame(
        ['Alice', 'Bob'],
        [
            {'Split', 'Steal'},
            {'Split', 'Steal'}
        ],
        {'A+0.5/B+0.5', 'A+0/B+1', 'A+1/B+0', 'A+0/B+0'},
        {
            ('Split', 'Split'): 'A+0.5/B+0.5',
            ('Split', 'Steal'): 'A+0/B+1',
            ('Steal', 'Split'): 'A+1/B+0',
            ('Steal', 'Steal'): 'A+0/B+0'
        }
    )

    m = {tuple(sp): gf.strategy_profile_to_outcome(sp) for sp in gf.strategy_profiles()}
    print(f'{m}')
