from time import time
from math import factorial
from time import time
from typing import List

with open('/home/user/Downloads/dataset_240280_2(3).txt', mode='r', encoding='utf-8') as f:
    data = f.read()

start_time = time()


expected_mass = 1200 # int(data.strip())
weights_table = [57, 71, 87, 97, 99, 101, 103, 113, 114, 115, 128, 129, 131, 137, 147, 156, 163, 186]
weights_table.sort(reverse=True)  # reverse so that it's largest to smallest

multipliers = [0] * len(weights_table)


# https://math.stackexchange.com/a/1356034
def permutations_without_dupes(multipliers: List[int]) -> int:
    numer = factorial(sum(multipliers))
    denom = 1
    for m in multipliers:
        denom *= factorial(m)
    return numer // denom


def exhaust(start_ptr: int, multipliers: List[int], total_sum: int, expected_sum: int) -> int:
    found = 0
    ptr = start_ptr
    while True:
        if total_sum >= expected_sum:
            if total_sum == expected_sum:
                found += permutations_without_dupes(multipliers)
            if start_ptr + 1 < len(multipliers):
                while multipliers[ptr] > 0:
                    multipliers[ptr] -= 1
                    total_sum -= weights_table[ptr]
                    found += exhaust(start_ptr+1, multipliers[:], total_sum, expected_sum)
            return found
        else:
            multipliers[ptr] += 1
            total_sum += weights_table[ptr]


# found = 5 -- [[1, 1, 0], [1, 0, 2], [0, 2, 1], [0, 1, 3], [0, 0, 5]]
found = exhaust(0, multipliers[:], 0, expected_mass)
print(f'{found}')














# expected_mass = 1024  # int(data.strip())
# weights_table = [57, 71, 87, 97, 99, 101, 103, 113, 114, 115, 128, 129, 131, 137, 147, 156, 163, 186]
# weights_table.sort(reverse=True)  # reverse so that it's largest to smallest
#
# multipliers = [0] * len(weights_table)
#
#
# # https://math.stackexchange.com/a/1356034
# def permutations_without_dupes(multipliers: List[int]) -> int:
#     numer = factorial(sum(multipliers))
#     denom = 1
#     for m in multipliers:
#         denom *= factorial(m)
#     return numer // denom
#
#
# def exhaust(start_ptr: int, multipliers: List[int]) -> int:
#     found = 0
#     ptr = start_ptr
#     while True:
#         total_sum = sum([a*b for a, b in zip(weights_table, multipliers)])
#         if total_sum >= expected_mass:
#             if total_sum == expected_mass:
#                 found += permutations_without_dupes(multipliers)
#             if start_ptr + 1 < len(multipliers):
#                 while multipliers[ptr] > 0:
#                     multipliers[ptr] -= 1
#                     found += exhaust(start_ptr+1, multipliers[:])
#             return found
#         else:
#             multipliers[ptr] += 1
#
#
# # found = 5 -- [[1, 1, 0], [1, 0, 2], [0, 2, 1], [0, 1, 3], [0, 0, 5]]
# found = exhaust(0, multipliers[:])
# print(f'{found}')






# expected_mass = 5  # int(data.strip())
# weights_table = [3, 2, 1]  # [57, 71, 87, 97, 99, 101, 103, 113, 114, 115, 128, 129, 131, 137, 147, 156, 163, 186]
# weights_table.sort(reverse=True)  # reverse so that it's largest to smallest
#
# multipliers = [0] * len(weights_table)
#
#
# def exhaust(start_ptr: int, multipliers: List[int], found: List[List[int]]):
#     ptr = start_ptr
#     while True:
#         total_sum = sum([a*b for a, b in zip(weights_table, multipliers)])
#         if total_sum >= expected_mass:
#             if total_sum == expected_mass:
#                 found.append(multipliers[:])
#             if start_ptr + 1 < len(multipliers):
#                 while multipliers[ptr] > 0:
#                     multipliers[ptr] -= 1
#                     exhaust(start_ptr+1, multipliers[:], found)
#             return
#         else:
#             multipliers[ptr] += 1
#
#
# found = []  # [[1, 1, 0], [1, 0, 2], [0, 2, 1], [0, 1, 3], [0, 0, 5]]
# exhaust(0, multipliers[:], found)
# print(f'{found}')







# class HashableCounter(Counter):
#     def __init__(self, v=None):
#         super().__init__(v)
#         self._cached_hash = None
#
#     def __hash__(self):
#         if self._cached_hash is None:
#             self._cached_hash = hash(tuple(sorted(self.items())))
#         return self._cached_hash
#
#     def __str__(self):
#         return '+'.join([str(k) + '*' + str(v) for k, v in sorted(self.items())])
#
#     def __repr__(self):
#         return str(self)
#
#
# cache = {0: {HashableCounter()}}
# all_cache = cache.copy()
#
# found = set()
# while len(cache) > 0:
#     new_cache = dict()
#     for mass, possibilities in cache.items():
#         for w in weights_table:
#             new_mass = mass + w
#             if new_mass > expected_mass:
#                 continue
#
#             distance_to_expected_mass = expected_mass - new_mass
#             if distance_to_expected_mass in all_cache:
#                 remainders = all_cache[distance_to_expected_mass]
#                 for r in remainders:
#                     for p in possibilities:
#                         p = HashableCounter(p + r)
#                         p[w] += 1
#                         found.add(p)
#             else:
#                 new_possibilities = set()
#                 for p in possibilities:
#                     p = HashableCounter(p)
#                     p[w] += 1
#                     new_possibilities.add(p)
#                 if new_mass < expected_mass:
#                     new_cache.setdefault(new_mass, set()).update(new_possibilities)
#                     all_cache.setdefault(new_mass, set()).update(new_possibilities)
#                 elif new_mass == expected_mass:
#                     found |= new_possibilities
#     cache = new_cache
#
#
# perms = []
# for f in found:
#     # https://math.stackexchange.com/a/1356034
#     numer = factorial(len(list(f.elements())))
#     denom = 1
#     for weight, count in f.items():
#         denom *= factorial(count)
#     permutations_without_dupes = numer // denom
#     print(f'{f} = {permutations_without_dupes}')
#     perms.append(permutations_without_dupes)
# print(f'{sum(perms)}')
#
#
print(f'{time() - start_time}')
