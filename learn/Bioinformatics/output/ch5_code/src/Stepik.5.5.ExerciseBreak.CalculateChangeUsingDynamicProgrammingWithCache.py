from functools import lru_cache
from typing import List
from helpers.HashableCollections import HashableList


# TAKES FOREVER WITHOUT A CACHE...
#
# def recursive_change(money: int, coins: List[int]):
#     if money == 0:
#         return 0
#     min_num_coins = None
#     for i in range(len(coins)):
#         if money >= coins[i]:
#             num_coins = recursive_change(money - coins[i], coins)
#             if min_num_coins is None or num_coins + 1 < min_num_coins:
#                 min_num_coins = num_coins + 1
#     return min_num_coins
#
#
# print(f'{recursive_change(76, [5, 4, 1])}')


@lru_cache(maxsize=65535)
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


for i in range(13, 22 + 1):
    print(f'{recursive_change(i, HashableList([5, 4, 1]))}')

# The problem wants you to manually cache the results so the algorithm doesn't recurse down the same path more than
# once. I automated this by using @lru_cache instead.
#
# You can use the coin counts for the first 12 elements directly given to you in the question to calculate the rest:
#
#                m = 0 1 2 3 4 5 6 7 8 9 10 11 12
# min_num_coins(m) = 0 1 2 3 1 1 2 3 2 2 2  3  3
#
# For example, since the coin denoms are 5, 4, and 1 (d={5,4,1}), to calculate min_num_coins for m=13, look up the
# result for anything where m+d=13. Given that d={5,4,1}, pull up the cached results for m=13-5=8, m=13-4=9, and
# m=13-1=12...
#   * for d=5, min_num_coins(13-5) = min_num_coins(8)  = 2
#   * for d=4, min_num_coins(13-4) = min_num_coins(9)  = 2
#   * for d=1, min_num_coins(13-1) = min_num_coins(12) = 3
# Since we're looking for the MINIMUM number of coins for m=13, we take the minimum of the results above and add one to
# it. 2 is the minimum result: You can either add a 5 coin (d=5) to the min_num_coins(8) or a 4 coin (d=4) to
# min_num_coins(9) to reach min_num_coins(13).
#
# Now that you have min_num_coins(13), you can add it to your cache and restart the process for min_num_coins(14).
# Stop after min_num_coins(22).


# On second thought, it may be better to use a cache directly and to build out that cache by computing from 0 to m. That
# way you don't bitten by overflowing the stack from recursion. See the CodeChallenge for 5.5 to see how that's
# implemented.
