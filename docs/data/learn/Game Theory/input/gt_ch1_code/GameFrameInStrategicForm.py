from itertools import product
from typing import Callable


class GameFrameInStrategicForm:
    def __init__(
            self,
            players: int,
            player_strategies: list[set[str]],
            outcomes: set[str],
            strategy_profile_to_outcome_func: Callable[[tuple[str, ...]], str]
    ):
        assert players >= 2
        assert player_strategies == player_strategies
        self.players = players
        self.player_strategies = player_strategies
        self.outcomes = outcomes
        self.strategy_profile_to_outcome_func = strategy_profile_to_outcome_func

    def enumerate_strategy_profiles(self):
        return list(product(*self.player_strategies))


if __name__ == '__main__':
    strategy_profile_to_outcome_map = {
        ('split', 'split'): '0.5 for 1, 0.5 for 2',
        ('split', 'steal'): '0.0 for 1, 1.0 for 2',
        ('steal', 'split'): '1.0 for 1, 0.0 for 2',
        ('steal', 'steal'): '0.0 for 1, 0.0 for 2'
    }

    gf = GameFrameInStrategicForm(
        2,
        [
            {'split', 'steal'},
            {'split', 'steal'}
        ],
        {
            '0.5 for 1, 0.5 for 2',
            '0.0 for 1, 1.0 for 2',
            '1.0 for 1, 0.0 for 2',
            '0.0 for 1, 0.0 for 2'
        },
        lambda sp: strategy_profile_to_outcome_map[sp]
    )

    print(f'{gf.enumerate_strategy_profiles()=}')
    print(f'{gf.strategy_profile_to_outcome_func(("steal", "steal"))=}')