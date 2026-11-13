from functools import lru_cache
from typing import List, Dict
from helpers.HashableCollections import HashableList

with open('/home/user/Downloads/dataset_240300_10(1).txt', mode='r', encoding='utf-8') as f:
    data = f.read()

lines = data.split('\n')
money = int(lines[0].strip())
coins = [int(c) for c in lines[1].strip().split(',')]


def recursive_change(money: int, coins: List[int], cache: Dict[int, int]):
    if money == 0:
        cache[money] = 0
        return cache[money]
    min_num_coins = None
    for i in range(len(coins)):
        if money >= coins[i]:
            num_coins = cache.get(money - coins[i])
            if num_coins is None:
                num_coins = recursive_change(money - coins[i], coins, cache)
            if min_num_coins is None or num_coins + 1 < min_num_coins:
                min_num_coins = num_coins + 1
    cache[money] = min_num_coins
    return cache[money]


cache = {}
for m in range(0, money):  # compute from 0 to money-1 to build out a cache
    recursive_change(m, coins, cache)
count = recursive_change(money, coins, cache)  # compute money from built out cache
print(f'{count}')


# There are 2 STOP and THINK questions on the next page...
#
# 1. If money = 109, DPChange requires a huge array of size 109. Modify the DPChange algorithm so that the array size
# required does not exceed the value of the largest coin denomination.
#
#   The code above calculates a cache by computing from 0 to m. As such, you only ever need to keep the last max(d)
#   elements in the cache. For example, since the coin denoms are 5, 4, and 1 (d={5,4,1}), to calculate min_num_coins
#   for m=13, look up the result for anything where m+d=13. Given that d={5,4,1}, pull up the cached results for
#   m=13-5=8, m=13-4=9, and m=13-1=12...
#     * for d=5, min_num_coins(13-5) = min_num_coins(8)  = 2
#     * for d=4, min_num_coins(13-4) = min_num_coins(9)  = 2
#     * for d=1, min_num_coins(13-1) = min_num_coins(12) = 3
#   In the above example, max(d) is 5 -- we're only ever looking up 5 slots back in the cache.
#
#   ALTERNATIVELY...
#
#   The STOP AND THINK section immediately following this problem asks how you can perform this exact same problem by
#   only keeping a cache up to the max coin denomination (e.g. if coin denom were 0.05, create cache with 0.01, 0.02,
#   0.03, 0.04, 0.05). I think this is possible by using modulo and division. For example, if 0.05 were the highest
#   denom, then take the input divide by 0.05 -- that'll tell you how many 0.05 coins you need in total. The remainder
#   will by less than 0.05 and you can use the cache to calculate that.
#
#   THE SECOND OPTION IS THE BETTER CHOICE IF IT WORKS.
#
# 2. Recall that our original goal was to make change, not just compute MinNumCoins(money). Modify DPChange so that it
# not only computes the minimum number of coins but also returns these coins.
#
#   I think it's pretty simple to change the algorithm to return an array of coin denominations vs just the count -- you
#   still have the count because the count is just the length of the array. Having said that, I haven't tried
#   implementing this yet.
