from sys import stdin

import yaml

from sequence_search import BurrowsWheelerTransform_FirstIndexes


# MARKDOWN_BUILD
class BWTRecord:
    __slots__ = ['first_ch', 'first_ch_cnt', 'last_ch', 'last_ch_cnt', 'last_to_first_ptr']

    def __init__(self, first_ch: str, first_ch_cnt: int, last_ch: str, last_ch_cnt: int, last_to_first_ptr: int):
        self.first_ch = first_ch
        self.first_ch_cnt = first_ch_cnt
        self.last_ch = last_ch
        self.last_ch_cnt = last_ch_cnt
        self.last_to_first_ptr = last_to_first_ptr


def to_bwt_with_first_indexes_checkpointed(
        seq: str,
        end_marker: str,
        first_indexes_checkpoint_n: int
) -> tuple[list[BWTRecord], dict[int, int]]:
    full_bwt_records = BurrowsWheelerTransform_FirstIndexes.to_bwt_with_first_indexes(seq, end_marker)
    bwt_records = []
    bwt_first_indexes_checkpoints = {}
    for i, rec in enumerate(full_bwt_records):
        if rec.first_idx % first_indexes_checkpoint_n == 0:
            bwt_first_indexes_checkpoints[i] = rec.first_idx
        new_rec = BWTRecord(rec.first_ch, rec.first_ch_cnt, rec.last_ch, rec.last_ch_cnt, rec.last_to_first_ptr)
        bwt_records.append(new_rec)
    return bwt_records, bwt_first_indexes_checkpoints
# MARKDOWN_BUILD


def main_build():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        data_raw = ''.join(stdin.readlines())
        data: dict = yaml.safe_load(data_raw)
        seq = data['sequence']
        end_marker = data['end_marker']
        first_indexes_checkpoint_n = data['first_indexes_checkpoint_n']
        print(f'Building BWT using the following settings...')
        print()
        print('```')
        print(data_raw)
        print('```')
        print()
        bwt_records, bwt_first_indexes_checkpoints = to_bwt_with_first_indexes_checkpointed(seq, end_marker, first_indexes_checkpoint_n)
        print()
        print(f'The following first and last columns were produced ...')
        print()
        print(f' * First: {[r.first_ch + str(r.first_ch_cnt) for r in bwt_records]}')
        print(f' * First Indexes Checkpoints: {bwt_first_indexes_checkpoints}')
        print(f' * Last: {[r.last_ch + str(r.last_ch_cnt) for r in bwt_records]}')
        print(f' * Last-to-First: {[r.last_to_first_ptr for r in bwt_records]}')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")










# MARKDOWN_WALK_BACK_TO_FIRST_IDX
def walk_back_until_first_indexes_checkpoint(
        bwt_records: list[BWTRecord],
        bwt_first_indexes_checkpoints: dict[int, int],
        row: int
) -> int:
    walk_cnt = 0
    while row not in bwt_first_indexes_checkpoints:
        row = bwt_records[row].last_to_first_ptr
        walk_cnt += 1
    first_idx = bwt_first_indexes_checkpoints[row] + walk_cnt
    # It's possible that the walk back continues backward before the start of the sequence, resulting
    # in it looping to the end and continuing to walk back from there. If that happens, the code below
    # adjusts it.
    sequence_len = len(bwt_records)
    if first_idx >= sequence_len:
        first_idx -= sequence_len
    return first_idx
# MARKDOWN_WALK_BACK_TO_FIRST_IDX


def main_walk_back_until_first_index_checkpoint():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        data_raw = ''.join(stdin.readlines())
        data: dict = yaml.safe_load(data_raw)
        first = data['first']
        last = data['last']
        last_to_first = data['last_to_first']
        bwt_first_indexes_checkpoints = data['first_indexes_checkpoints']
        from_row = data['from_row']
        print(f'Building BWT using the following settings...')
        print()
        print('```')
        print(data_raw)
        print('```')
        print()
        bwt_records = []
        for (first_ch, first_ch_cnt), (last_ch, last_ch_cnt), last_to_first_ptr in zip(first, last, last_to_first):
            bwt_records.append(BWTRecord(first_ch, first_ch_cnt, last_ch, last_ch_cnt, last_to_first_ptr))
        first_idx = walk_back_until_first_indexes_checkpoint(bwt_records, bwt_first_indexes_checkpoints, from_row)
        print(f'Walking back to a first index checkpoint resulted in a first index of {first_idx} ...')
        print()
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")












# MARKDOWN_TEST
def walk_find(
        bwt_records: list[BWTRecord],
        bwt_first_indexes_checkpoints: dict[int, int],
        test: str,
        start_row: int
) -> int | None:
    row = start_row
    for ch in reversed(test[:-1]):
        if bwt_records[row].last_ch != ch:
            return None
        row = bwt_records[row].last_to_first_ptr
    first_idx = walk_back_until_first_indexes_checkpoint(bwt_records, bwt_first_indexes_checkpoints, row)
    return first_idx


def find(
        bwt_records: list[BWTRecord],
        bwt_first_indexes_checkpoints: dict[int, int],
        test: str
) -> list[int]:
    found = []
    for i, rec in enumerate(bwt_records):
        if rec.first_ch == test[-1]:
            if len(test) == 1:
                first_idx = walk_back_until_first_indexes_checkpoint(bwt_records, bwt_first_indexes_checkpoints, i)
                found.append(first_idx)
            elif rec.last_ch == test[-2]:
                found_idx = walk_find(bwt_records, bwt_first_indexes_checkpoints, test, i)
                if found_idx is not None:
                    found.append(found_idx)
    return found
# MARKDOWN_TEST


def main_test():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        data_raw = ''.join(stdin.readlines())
        data: dict = yaml.safe_load(data_raw)
        first = data['first']
        last = data['last']
        last_to_first = data['last_to_first']
        bwt_first_indexes_checkpoints = data['first_indexes_checkpoints']
        test = data['test']
        print(f'Building BWT using the following settings...')
        print()
        print('```')
        print(data_raw)
        print('```')
        print()
        bwt_records = []
        for (first_ch, first_ch_cnt), (last_ch, last_ch_cnt), last_to_first_ptr in zip(first, last, last_to_first):
            bwt_records.append(BWTRecord(first_ch, first_ch_cnt, last_ch, last_ch_cnt, last_to_first_ptr))
        found_indices = find(bwt_records, bwt_first_indexes_checkpoints, test)
        print()
        print(f'*{test}* found at indices {found_indices}.')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")










if __name__ == '__main__':
    main_build()
