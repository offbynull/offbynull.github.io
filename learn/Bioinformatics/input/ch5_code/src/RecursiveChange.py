from typing import List


def recursive_change(money: int, coins: List[int]):
    if money == 0:
        return 0
    min_num_coins = None
    for i in range(len(coins)):
        if money >= coins[i]:
            num_coins = recursive_change(money - coins[i], coins)
            if min_num_coins is None or num_coins + 1 < min_num_coins:
                min_num_coins = num_coins + 1
    return min_num_coins


print(f'{recursive_change(76, [5, 4, 1])}')