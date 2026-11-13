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





with open('/home/user/Downloads/dataset_240379_2.txt', mode='r', encoding='utf-8') as f:
    data = f.read()
data = [l.strip() for l in data.strip().split('\n')]
text = data[0]
# text = 'panamabananas$'
suffix_array = construct_suffix_array(text)
# for i, val in suffix_array:
#     print(f'{i} {val}')
print(f'{" ".join(str(e[0]) for e in suffix_array)}')


