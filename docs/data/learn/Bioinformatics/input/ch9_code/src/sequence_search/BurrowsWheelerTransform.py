import functools
from collections import Counter

from helpers.Utils import rotate_right
from sequence_search.SearchUtils import StringView


# MARKDOWN_BUILD
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


def to_bwt(
        seq: StringView,
        end_marker: StringView
):
    assert end_marker == seq[-1], f'{seq} missing end marker'
    assert end_marker not in seq[:-1], f'{seq} has end marker but not at the end'
    sorted_rotations = sorted(
        rotate_right(seq),
        key=functools.cmp_to_key(lambda a, b: cmp(a, b, end_marker))
    )
    first_ch_counter = Counter()
    last_ch_counter = Counter()
    ret = []
    for i, s in enumerate(sorted_rotations):
        first_ch = s[0]
        first_ch_counter[first_ch] += 1
        first_ch_cnt = first_ch_counter[first_ch]
        last_ch = s[-1]
        last_ch_counter[last_ch] += 1
        last_ch_cnt = last_ch_counter[last_ch]
        ret.append(((first_ch, first_ch_cnt), (last_ch, last_ch_cnt)))
    return ret
# MARKDOWN_BUILD


res = to_bwt(
    StringView.wrap('panamabananas$'),
    StringView.wrap('$')
)
for e in res:
    print(f'{e}')