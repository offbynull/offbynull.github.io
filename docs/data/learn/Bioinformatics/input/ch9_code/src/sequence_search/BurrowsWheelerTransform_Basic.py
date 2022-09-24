import functools
from collections import Counter
from sys import stdin

import yaml

from sequence_search.SearchUtils import RotatedListView


# MARKDOWN_BUILD_MATRIX
def cmp(a: list[tuple[str, int]], b: list[tuple[str, int]], end_marker: str):
    if len(a) != len(b):
        raise '???'
    for (a_ch, _), (b_ch, _) in zip(a, b):
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
    return 0


def to_bwt_matrix(
        seq: str,
        end_marker: str
) -> list[RotatedListView]:
    assert end_marker == seq[-1], f'{seq} missing end marker'
    assert end_marker not in seq[:-1], f'{seq} has end marker but not at the end'
    # Create matrix
    seq_with_counts = []
    seq_ch_counter = Counter()
    for ch in seq:
        seq_ch_counter[ch] += 1
        ch_cnt = seq_ch_counter[ch]
        seq_with_counts.append((ch, ch_cnt))
    seq_with_counts_rotations = [RotatedListView(i, seq_with_counts) for i in range(len(seq_with_counts))]
    seq_with_counts_rotations_sorted = sorted(
        seq_with_counts_rotations,
        key=functools.cmp_to_key(lambda a, b: cmp(a, b, end_marker))
    )
    return seq_with_counts_rotations_sorted
# MARKDOWN_BUILD_MATRIX


def main_build_matrix():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        data_raw = ''.join(stdin.readlines())
        data: dict = yaml.safe_load(data_raw)
        seq = data['sequence']
        end_marker = data['end_marker']
        print(f'Building BWT matrix using the following settings...')
        print()
        print('```')
        print(data_raw)
        print('```')
        print()
        bwt_matrix = to_bwt_matrix(seq, end_marker)
        print()
        print(f'The following BWT matrix was produced ...')
        print()
        print('<table>')
        for r in bwt_matrix:
            r_str = '<tr><td>' + '</td><td>'.join(f'({ch},{c})' for ch, c in r) + '</td></tr>'
            print(r_str)
        print('</table>')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")













# MARKDOWN_FIRST_LAST
def get_bwt_first_and_last_columns(
        seq: str,
        end_marker: str
) -> tuple[list[tuple[str, int]], list[tuple[str, int]]]:
    bwt_matrix = to_bwt_matrix(seq, end_marker)
    first = []
    last = []
    for s in bwt_matrix:
        first.append(s[0])
        last.append(s[-1])
    return first, last
# MARKDOWN_FIRST_LAST


def main_first_and_last_columns():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        data_raw = ''.join(stdin.readlines())
        data: dict = yaml.safe_load(data_raw)
        seq = data['sequence']
        end_marker = data['end_marker']
        print(f'Building BWT using the following settings...')
        print()
        print('```')
        print(data_raw)
        print('```')
        print()
        first, last = get_bwt_first_and_last_columns(seq, end_marker)
        print()
        print(f'The following BWT first and last columns were produced ...')
        print()
        print(f' * {first=}')
        print(f' * {last=}')
        print()
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")










# MARKDOWN_WALK
def walk(
        first: list[tuple[str, int]],
        last: list[tuple[str, int]]
) -> str:
    ret = ''
    row = 0  # first idx always has first_ch == end_marker because of the lexicographical sorting
    while True:
        last_ch, last_ch_cnt = last[row]
        ret += last_ch
        row = next(i for i, (first_ch, first_ch_cnt) in enumerate(first) if first_ch == last_ch and first_ch_cnt == last_ch_cnt)
        if row == 0:
            break
    ret = ret[::-1]  # reverse ret
    ret = ret[1:] + ret[0]  # ret has end_marker at beginning, rotate it to end
    return ret
# MARKDOWN_WALK


def main_walk():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        data_raw = ''.join(stdin.readlines())
        data: dict = yaml.safe_load(data_raw)
        first = data['first']
        last = data['last']
        print(f'Building BWT using the following settings...')
        print()
        print('```')
        print(data_raw)
        print('```')
        print()
        seq = walk(first, last)
        print()
        print(f'The original sequence was *{seq}*.')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")





















# MARKDOWN_TEST
def walk_find(
        first: list[tuple[str, int]],
        last: list[tuple[str, int]],
        test: str,
        start_row: int
) -> bool:
    row = start_row
    for ch in reversed(test[:-1]):
        last_ch, last_ch_cnt = last[row]
        if last_ch != ch:
            return False
        row = next(i for i, (first_ch, first_ch_cnt) in enumerate(first) if first_ch == last_ch and first_ch_cnt == last_ch_cnt)
    return True


def find(
        first: list[tuple[str, int]],
        last: list[tuple[str, int]],
        test: str
) -> int:
    found = 0
    for i, (first_ch, _) in enumerate(first):
        if first_ch == test[-1] and walk_find(first, last, test, i):
            found += 1
    return found
    # The code above is the obvious way to do this. However, since the first column is always sorted by character, the
    # entire array doesn't need to be scanned. Instead, you can binary search to the first and last index with
    # first_ch == test[-1] and just consider those indices.
# MARKDOWN_TEST


def main_test():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        data_raw = ''.join(stdin.readlines())
        data: dict = yaml.safe_load(data_raw)
        test = data['test']
        first = data['first']
        last = data['last']
        print(f'Building BWT using the following settings...')
        print()
        print('```')
        print(data_raw)
        print('```')
        print()
        found_cnt = find(first, last, test)
        print()
        print(f'*{test}* found {found_cnt} times.')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")



if __name__ == '__main__':
    main_test()
