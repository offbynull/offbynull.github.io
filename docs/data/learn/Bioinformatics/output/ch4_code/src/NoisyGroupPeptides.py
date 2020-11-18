import typing
from collections import Counter
from typing import List

from Utils import rotate, HashableList, N


def group_peptides_within_tolerance(p_list: List[List[N]], pos_tolerance: float) -> typing.Counter[List[float]]:
    p_list_sums = [(p, sum(p)) for p in p_list]
    p_list_sums.sort(key=lambda p: p[1])
    length = len(p_list_sums)
    ret = Counter()
    for i, p_packed in enumerate(p_list_sums):
        p1, p1_sum = p_packed
        # search backwards
        left_limit = 0
        for j in range(i, -1, -1):
            p2, p2_sum = p_list_sums[j]
            if abs(p1_sum - p2_sum) > pos_tolerance * len(p1):
                left_limit = j
                break
        # search forwards
        right_limit = length - 1
        for j in range(i, length):
            p2, p2_sum = p_list_sums[j]
            if abs(p1_sum - p2_sum) > pos_tolerance * len(p1):
                right_limit = j
                break
        for j in range(left_limit, right_limit + 1):
            p2, p2_sum = p_list_sums[j]
            if len(p1) != len(p2):
                continue
            for p2_rotated in rotate(p2):
                max_idx_dist = max(abs(aa2 - aa1) for aa1, aa2 in zip(p1, p2_rotated))
                if max_idx_dist <= pos_tolerance:
                    ret[HashableList(p1)] += 1
                    break
    return ret


if __name__ == '__main__':
    print(f'{group_peptides_within_tolerance([[1.1, 2, 3, 4], [0, 1, 0], [3, 4, 1, 1], [2, 0, 0], [1]], 3)}')
    print(f'{group_peptides_within_tolerance([[1, 2, 3, 4], [0, 1, 0], [3, 4, 1, 1], [2, 0, 0], [1]], 3)}')