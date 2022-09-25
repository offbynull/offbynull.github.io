from sys import stdin

import yaml

from sequence_search.BurrowsWheelerTransform_Basic_LastToFirst import BWTRecord
from sequence_search.BurrowsWheelerTransform_Deserialization import to_bwt_optimized2


# MARKDOWN_TEST
def find(
        bwt_records: list[BWTRecord],
        test: str
) -> int:
    top = 0
    bottom = len(bwt_records) - 1
    for ch in reversed(test):
        # Scan down to find new top, which is the first instance of ch (lowest symbol instance count for ch)
        new_top = len(bwt_records)
        for i in range(top, bottom + 1):
            record = bwt_records[i]
            if ch == record.last_ch:
                new_top = record.last_to_first_ptr
                break
        # Scan up to find new bottom, which is the last instance of ch (highest symbol instance count for ch)
        new_bottom = -1
        for i in range(bottom, top - 1, -1):
            record = bwt_records[i]
            if ch == record.last_ch:
                new_bottom = record.last_to_first_ptr
                break
        # Check if not found
        if new_bottom == -1 or new_top == len(bwt_records):  # technically only need to check one of these conditions
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
        print(f' * First: {[(r.first_ch, r.first_ch_cnt) for r in bwt_records]}')
        print(f' * Last: {[(r.last_ch, r.last_ch_cnt) for r in bwt_records]}')
        print(f' * Last-to-First: {[r.last_to_first_ptr for r in bwt_records]}')
        print()
        found_cnt = find(bwt_records, test)
        print()
        print(f'*{test}* found in *{seq}* {found_cnt} times.')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")











if __name__ == '__main__':
    main_test()
