`{bm-disable-all}`[ch9_code/src/sequence_search/BurrowsWheelerTransform_Basic.py](ch9_code/src/sequence_search/BurrowsWheelerTransform_Basic.py) (lines 12 to 214):`{bm-enable-all}`

```python
def cmp(a: str, b: str, end_marker: str):
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


class BWTRecord:
    __slots__ = ['first_ch', 'first_ch_idx', 'last_ch', 'last_ch_idx', 'last_to_first_idx']

    def __init__(self, first_ch: str, first_ch_idx: int, last_ch: str, last_ch_idx: int):
        self.first_ch = first_ch
        self.first_ch_idx = first_ch_idx
        self.last_ch = last_ch
        self.last_ch_idx = last_ch_idx
        self.last_to_first_idx = -1

    def __str__(self):
        return str((self.first_ch + str(self.first_ch_idx), self.last_ch + str(self.last_ch_idx), self.last_to_first_idx))

    def __repr__(self):
        return str(self)


def to_bwt(
        seq: str,
        end_marker: str
) -> list[BWTRecord]:
    assert end_marker == seq[-1], f'{seq} missing end marker'
    assert end_marker not in seq[:-1], f'{seq} has end marker but not at the end'
    rotations_with_counts = zip(
        rotate_right(seq),
        range(len(seq))
    )
    rotations_with_counts_sorted = sorted(
        rotations_with_counts,
        key=functools.cmp_to_key(lambda a, b: cmp(a[0], b[0], end_marker))
    )
    first_ch_counter = Counter()
    last_ch_counter = Counter()
    ret = []
    for i, (s, idx) in enumerate(rotations_with_counts_sorted):
        first_ch = s[0]
        first_ch_counter[first_ch] += 1
        first_ch_idx = first_ch_counter[first_ch]
        last_ch = s[-1]
        last_ch_counter[last_ch] += 1
        last_ch_idx = last_ch_counter[last_ch]
        record = BWTRecord(first_ch, first_ch_idx, last_ch, last_ch_idx)
        ret.append(record)
    for i, record_a in enumerate(ret):
        last = record_a.last_ch, record_a.last_ch_idx
        for j, record_b in enumerate(ret):
            first = record_b.first_ch, record_b.first_ch_idx
            if last == first:
                record_a.last_to_first_idx = j
                break
    return ret
# MARKDOWN_BUILD


def main_build():
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
        bwt_records = to_bwt(seq, end_marker)
        print()
        print(f'The following first and last columns were produced ...')
        print()
        print(f' * First: {[r.first_ch + str(r.first_ch_idx) for r in bwt_records]}')
        print(f' * Last: {[r.last_ch + str(r.last_ch_idx) for r in bwt_records]}')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")








# MARKDOWN_DESERIALIZE
def cmp_instances(a: tuple[str, int], b: tuple[str, int], end_marker: str):
    # compare symbol
    x = cmp(a[0], b[0], end_marker)
    if x != 0:
        return x
    # compare symbol instance count
    if a[1] < b[1]:
        return -1
    elif a[1] > b[1]:
        return 1
    return 0


def to_bwt_from_last_sequence(
        last_seq: str,
        end_marker: str
) -> list[BWTRecord]:
    ret = []
    last_col = [(last_ch, last_ch_idx + 1) for last_ch_idx, last_ch in enumerate(last_seq)]
    first_col = sorted(last_col, key=functools.cmp_to_key(lambda a, b: cmp(a, b, end_marker)))
    for (first_ch, first_ch_idx), (last_ch, last_ch_idx) in zip(first_col, last_col):
        record = BWTRecord(first_ch, first_ch_idx, last_ch, last_ch_idx)
        ret.append(record)
    for i, record_a in enumerate(ret):
        last = record_a.last_ch, record_a.last_ch_idx
        for j, record_b in enumerate(ret):
            first = record_b.first_ch, record_b.first_ch_idx
            if last == first:
                record_a.last_to_first_idx = j
                break
    return ret
# MARKDOWN_DESERIALIZE


def main_deserialize():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        data_raw = ''.join(stdin.readlines())
        data: dict = yaml.safe_load(data_raw)
        last_seq = data['last_seq']
        end_marker = data['end_marker']
        print(f'Deserializing BWT using the following settings...')
        print()
        print('```')
        print(data_raw)
        print('```')
        print()
        bwt_records = to_bwt_from_last_sequence(last_seq, end_marker)
        print()
        print(f'The following first and last columns were produced ...')
        print()
        print(f' * First: {[r.first_ch + str(r.first_ch_idx) for r in bwt_records]}')
        print(f' * Last: {[r.last_ch + str(r.last_ch_idx) for r in bwt_records]}')
        print()
        seq = walk(bwt_records)
        print()
        print(f'The original sequence reconstructed from the BWT array: *{seq}*.')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")







def to_bwt_from_first_last_cols(
        first_col: list[list[Any]],
        last_col: list[list[Any]]
) -> list[BWTRecord]:
    ret = []
    for first, last in zip(first_col, last_col):
        record = BWTRecord(first[0], first[1], last[0], last[1])
        ret.append(record)
    for i, record_a in enumerate(ret):
        last = record_a.last_ch, record_a.last_ch_idx
        for j, record_b in enumerate(ret):
            first = record_b.first_ch, record_b.first_ch_idx
            if last == first:
                record_a.last_to_first_idx = j
                break
    return ret


# MARKDOWN_WALK
def walk(bwt_array: list[BWTRecord]) -> str:
    ret = ''
    row = 0  # first idx of bwt_array always has first_ch == end_marker because of the lexicographical sorting
    while True:
        ret += bwt_array[row].last_ch
        row = bwt_array[row].last_to_first_idx
        if row == 0:
            break
    ret = ret[::-1]  # reverse ret
    ret = ret[1:] + ret[0]  # ret has end_marker at beginning, rotate it to end
    return ret
```