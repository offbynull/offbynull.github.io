from sys import stdin

import yaml

from sequence_search.BurrowsWheelerTransform_Basic import BWTRecord


# MARKDOWN_TEST
from sequence_search.BurrowsWheelerTransform_Deserialization import to_bwt_optimized2


def find(
        bwt_array: list[BWTRecord],
        test: str
) -> int:
    top = 0
    bottom = len(bwt_array) - 1
    for ch in reversed(test):
        new_top = len(bwt_array)
        new_bottom = -1
        for i in range(top, bottom + 1):
            record = bwt_array[i]
            if ch == record.last_ch:
                new_top = min(new_top, record.last_to_first_idx)
                new_bottom = max(new_bottom, record.last_to_first_idx)
        if new_bottom == -1 or new_top == len(bwt_array):  # technically only need to check one of these conditions
            return 0
        top = new_top
        bottom = new_bottom
    return (bottom - top) + 1
# MARKDOWN_TEST


def main_test():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        data_raw = ''.join(stdin.readlines())
        data: dict = yaml.safe_load(data_raw)
        test = data['test']
        seq = data['sequence']
        end_marker = data['end_marker']
        print(f'Building BWT using the following settings...')
        print()
        print('```')
        print(data_raw)
        print('```')
        print()
        bwt_records = to_bwt_optimized2(seq, end_marker)
        print()
        print(f'The following first and last columns were produced ...')
        print()
        print(f' * First: {[r.first_ch + str(r.first_ch_idx) for r in bwt_records]}')
        print(f' * Last: {[r.last_ch + str(r.last_ch_idx) for r in bwt_records]}')
        print()
        found_cnt = find(bwt_records, test)
        print()
        print(f'*{test}* found in *{seq}* {found_cnt} times.')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")











if __name__ == '__main__':
    main_test()