import functools


def cmp(v1: tuple[int, str], v2: tuple[int, str]):
    a = v1[1]
    b = v2[1]
    for a_ch, b_ch in zip(a, b):
        if a_ch == '$' and b_ch == '$':
            continue
        if a_ch == '$':
            return -1
        if b_ch == '$':
            return 1
        if a_ch < b_ch:
            return -1
        if a_ch > b_ch:
            return 1
    if len(a) < len(b):
        return a
    elif len(b) < len(a):
        return b
    raise '???'


def construct_suffix_array(text: str):
    ret = []
    for i in range(len(text) - 1, -1, -1):
        region = text[i:]
        ret.append((i, region))
    ret = sorted(ret, key=functools.cmp_to_key(cmp))
    return ret





with open('/home/user/Downloads/dataset_240390_2.txt', mode='r', encoding='utf-8') as f:
    data = f.read()
data = [l.strip() for l in data.strip().split('\n')]
text = data[0]
multiple = int(data[1])
suffix_array = construct_suffix_array(text)
partial_suffix_array = [(i, idx_in_text) for i, (idx_in_text, _) in enumerate(suffix_array) if idx_in_text % multiple == 0]
for i, idx_in_text in partial_suffix_array:
    print(f'{i} {idx_in_text}')


