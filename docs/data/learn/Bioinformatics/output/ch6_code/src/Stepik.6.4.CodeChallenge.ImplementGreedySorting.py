from typing import List

with open('/home/user/Downloads/dataset_240319_4.txt', mode='r', encoding='utf-8') as f:
    data = f.read()

lines = data.split('\n')
signed_permutation = [int(i) for i in lines[0].split()]


def greedy_sorting(p: List[int]):
    p = p[:]
    for start in range(0, len(p)):
        k = start + 1
        # is the correct value in the correct slot already? skip
        if p[start] == k:
            continue
        # find where the correct value is
        end = -1
        for i, v in enumerate(p[start:]):
            if v == k or v == -k:
                end = start + i
                break
        # reverse the elements between start and end + negate each one, putting the correct value at start (although it might be negative) -- +1 STEPS
        p[start:end+1] = [-x for x in reversed(p[start:end+1])]
        yield p
        # if the newly placed correct value is negative, make it positive -- +1 STEPS
        if p[start] < 0:
            p[start] = -p[start]
            yield p


for p in greedy_sorting(signed_permutation):
    print(f'{" ".join(("+" if k >= 0 else "") + str(k) for k in p)}')
