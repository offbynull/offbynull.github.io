from abc import ABC, abstractmethod
from itertools import product

from GameFrame import GameFrame, MappedOutcomesGameFrame


class OrdinalGame(ABC):
    def __init__(self, game_frame: GameFrame):
        self.game_frame = game_frame

    @abstractmethod
    def player_outcome_preference(self, player: int, outcome: str) -> int:
        ...


class MappedPreferencesOrdinalGame(OrdinalGame):
    def __init__(
            self,
            game_frame: GameFrame,
            player_preference_rankings: dict[int, dict[str, int]]  # player num -> (outcome -> preference)
    ):
        super().__init__(game_frame)
        self.player_preference_rankings = player_preference_rankings

    def player_outcome_preference(self, player: int, outcome: str) -> int:
        return self.player_preference_rankings[player][outcome]


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
    og = MappedPreferencesOrdinalGame(
        gf,
        {
            0: {
                'A+0.5/B+0.5': 1,
                'A+0/B+1': 0,
                'A+1/B+0': 2,
                'A+0/B+0': 0
            },
            1: {
                'A+0.5/B+0.5': 1,
                'A+0/B+1': 2,
                'A+1/B+0': 0,
                'A+0/B+0': 0
            }
        }
    )

    m = {(p, o): og.player_outcome_preference(p, o) for (p, _), o in product(enumerate(og.game_frame.players), og.game_frame.outcomes)}
    print(f'{m}')