import functools

from helpers.Utils import slide_window


def cmp(a: str, b: str):
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
        return -1
    elif len(b) < len(a):
        return 1
    return 0


def bwt(text: str):
    matrix = [t for t, _ in slide_window(text, len(text), cyclic=True)]
    matrix.sort(key=functools.cmp_to_key(cmp))
    return ''.join(row[-1] for row in matrix)





with open('/home/user/Downloads/dataset_240380_5.txt', mode='r', encoding='utf-8') as f:
    data = f.read()
data = [l.strip() for l in data.strip().split('\n')]
text = data[0]
# text = 'panamabananas$'
result = bwt(text)
print(result)


