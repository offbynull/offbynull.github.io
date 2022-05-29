`{bm-disable-all}`[ch9_code/src/sequence_search/SuffixArray.py](ch9_code/src/sequence_search/SuffixArray.py) (lines 13 to 43):`{bm-enable-all}`

```python
def cmp(a: StringView, b: StringView, end_marker: StringView):
    for a_ch, b_ch in zip(a, b):
        if a_ch == end_marker and b_ch == end_marker:
            continue
        if a_ch == end_marker:
            return -1
        if b_ch == end_marker:
            return 1
        if a_ch < b_ch:
            return -1
        if a_ch > b_ch:
            return 1
    if len(a) < len(b):
        return 1
    elif len(a) > len(b):
        return -1
    raise '???'


def to_suffix_array(
        seq: StringView,
        end_marker: StringView
):
    assert end_marker == seq[-1], f'{seq} missing end marker'
    assert end_marker not in seq[:-1], f'{seq} has end marker but not at the end'
    ret = []
    while len(seq) > 0:
        ret.append(seq)
        seq = seq[1:]
    ret = sorted(ret, key=functools.cmp_to_key(lambda a, b: cmp(a, b, end_marker)))
    return ret
```