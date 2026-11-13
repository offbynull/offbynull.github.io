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
    # MARKDOWN_STRICT_DOMINANCE

    # MARKDOWN_WEAK_DOMINANCE
    def weakly_dominates_other(self, player: int, strategy1: str, strategy2: str) -> bool:
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

    # MARKDOWN_EQUIVALENT
    def equivalent_to_other(self, player: int, strategy1: str, strategy2: str) -> bool:
        for player_strategy_profile in product(*(s if i != player else {'FAKE'} for i, s in enumerate(self.strategies))):
            player_strategy_profile_1 = list(player_strategy_profile)
            player_strategy_profile_2 = list(player_strategy_profile)
            player_strategy_profile_1[player] = strategy1
            player_strategy_profile_2[player] = strategy2
            payoff_1 = self.player_strategy_profile_preference(player, tuple(player_strategy_profile_1))
            payoff_2 = self.player_strategy_profile_preference(player, tuple(player_strategy_profile_2))
            if not (payoff_1 == payoff_2):
                return False
        return True
    # MARKDOWN_EQUIVALENT

    # MARKDOWN_STRICT_DOMINANCE_TOTAL
    def strictly_dominates_overall(self, player: int, strategy: str) -> bool:
        for other_strategy in self.strategies[player]:
            if strategy == other_strategy:
                continue
            if not self.strictly_dominates_other(player, strategy, other_strategy):
                return False
        return True
    # MARKDOWN_STRICT_DOMINANCE_TOTAL

    # MARKDOWN_WEAK_DOMINANCE_TOTAL
    def weakly_dominates_overall(self, player: int, strategy: str) -> bool:
        for other_strategy in self.strategies[player]:
            if strategy == other_strategy:
                continue
            if not self.weakly_dominates_other(player, strategy, other_strategy) \
                    and not self.equivalent_to_other(player, strategy, other_strategy):
                return False
        return True
    # MARKDOWN_WEAK_DOMINANCE_TOTAL

    # MARKDOWN_STRICTLY_DOMINANT_STRATEGY_EQUILIBRIUM
    def strictly_dominant_strategy_equilibrium(self, strategy_profile: list[str]):
        for i, _ in enumerate(self.players):
            if not self.strictly_dominates_overall(i, strategy_profile[i]):
                return False
        return True
    # MARKDOWN_STRICTLY_DOMINANT_STRATEGY_EQUILIBRIUM

    # MARKDOWN_WEAKLY_DOMINANT_STRATEGY_EQUILIBRIUM
    def weakly_dominant_strategy_equilibrium(self, strategy_profile: list[str]):
        found_strict_dom = False
        for i, _ in enumerate(self.players):
            if not self.weakly_dominates_overall(i, strategy_profile[i]):
                return False
            found_strict_dom = self.strictly_dominates_overall(i, strategy_profile[i])
        return found_strict_dom
    # MARKDOWN_WEAKLY_DOMINANT_STRATEGY_EQUILIBRIUM

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
    print(f'{og.strictly_dominant_strategy_equilibrium(["Lie", "Lie"])}')
    print(f'{og.weakly_dominant_strategy_equilibrium(["Lie", "Lie"])}')
    # print(f'{og.is_weakly_dominant(0, "Get Violent", "Lie")}')
    # print(f'{og.is_weakly_dominant(0, "Get Violent", "Stay Silent")}')
    # print(f'{og.is_weakly_dominant(0, "Lie", "Stay Silent")}')
    # m = {(p, tuple(sp)): og.player_strategy_profile_preference(p, tuple(sp)) for (p, _), sp in product(enumerate(og.players), og.strategy_profiles())}
    # print(f'{m}')