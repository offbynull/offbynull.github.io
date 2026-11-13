from math import log2, floor
from typing import List, Optional

# NO ALGORITHM WAS GIVEN FOR THIS PROBLEM, BUT https://users.cs.fiu.edu/~weiss/cop3337_f99/assignments/turnpike.pdf
# DESCRIBES A RECURSIVE ALGORITHM YOU CAN USE. THAT'S WHAT I USED HERE.
#
# THE BOOK DOESN'T LAY OUT WHAT PROBLEM THIS IS TRYING TO SOLVE. MY GUESS IS THAT IT HAS SOMETHING TO DO WITH
# CONVOLUTIONS, SINCE CONVOLUTIONS ARE USED TO FIND POSSIBLE AMINO ACID MASSES BY DIFFERENCING SPECTRUM MASSES AND THIS
# IS REVERSING FROM DIFFERENCES TO THE ORIGINAL NUMBERS THAT WERE DIFFERENCED.

with open('/home/user/Downloads/dataset_240294_1.txt', mode='r', encoding='utf-8') as f:
    data = f.read()

diffs = [int(d) for d in data.strip().split()]
dists = list(filter(lambda x: x > 0, diffs))


def get_orig_len_from_dists_len(dists_len: int) -> int:
    # Try to derive n from |D| for |D| = n(n-1)/2
    #
    # |D| = n(n-1)/2
    # 2*|D| = n(n-1)  multiply both sides by 2
    test_num = log2(2 * dists_len)  # since 2*|D| = n(n-1), get log2(2*|D|), because n^2 > n(n-1)

    # Starting from floor(test_num), test upwards until you find a match to |D|
    test_num = floor(test_num)
    while test_num * (test_num - 1) / 2 < dists_len:
        test_num += 1
    assert test_num * (test_num - 1) / 2 == dists_len
    return test_num


def get_diff_pairs(orig: List[int]) -> List[int]:
    dists = []
    for o1 in orig:
        for o2 in orig:
            diff = o2-o1
            if diff > 0:
                dists.append(diff)
    dists.sort()
    return dists


def test_and_remove_if_diffs_exist(
        val: int,
        orig: List[int],
        orig_lo: int,
        orig_hi: int,
        dists: List[int]
) -> Optional[List[int]]:
    new_dists = dists[:]
    if val not in new_dists:
        return None
    new_dists.remove(val)
    for i in range(0, orig_lo):
        diff = abs(orig[i] - val)
        if diff not in new_dists:
            return None
        new_dists.remove(diff)
    for i in range(orig_hi - 1, len(orig)):
        diff = abs(orig[i] - val)
        if diff not in new_dists:
            return None
        new_dists.remove(diff)
    return new_dists


def recurse(
        orig: List[int],
        orig_lo: int,
        orig_hi: int,
        dists: List[int]
) -> bool:
    if len(dists) == 0:
        return True
    dist = dists[-1]
    new_lo_val = orig[-1] - dist
    new_dists = test_and_remove_if_diffs_exist(new_lo_val, orig, orig_lo, orig_hi, dists)
    if new_dists is not None:
        orig[orig_lo] = new_lo_val
        found = recurse(orig, orig_lo + 1, orig_hi, new_dists)
        if found:
            return found
    new_hi_val = dist
    new_dists = test_and_remove_if_diffs_exist(new_hi_val, orig, orig_lo, orig_hi, dists)
    if new_dists is not None:
        orig[orig_hi - 2] = new_hi_val
        found = recurse(orig, orig_lo, orig_hi - 1, new_dists)
        if found:
            return found
    return False


orig_len = get_orig_len_from_dists_len(len(dists))
orig = [0] * orig_len
orig[-1] = dists.pop()

recurse(orig, 0, len(orig), dists)
orig.sort()

print(f'{" ".join([str(i) for i in orig])}')