`{bm-disable-all}`[ch9_code/src/sequence_search/BurrowsWheelerTransform_Basic.py](ch9_code/src/sequence_search/BurrowsWheelerTransform_Basic.py) (lines 184 to 239):`{bm-enable-all}`

```python
def walk_find(
        bwt_array: list[BWTRecord],
        test: str,
        start_row: int
) -> bool:
    row = start_row
    for ch in reversed(test[:-1]):
        if bwt_array[row].last_ch != ch:
            return False
        row = bwt_array[row].last_to_first_idx
    return True


def find(
        bwt_array: list[BWTRecord],
        test: str
) -> int:
    found = 0
    for i, rec in enumerate(bwt_array):
        if rec.first_ch == test[-1]:
            if len(test) == 1 or (rec.last_ch == test[-2] and walk_find(bwt_array, test, i)):
                found += 1
    return found
    # The code above is the obvious way to do this. However, since the first column is always sorted by character, the
    # entire array doesn't need to be scanned. Instead, you can binary search to the first and last index with
    # rec.first_ch == test[-1] and just consider those indices.
    #
    # The problem with doing this is that bisect_left/bisect_right has a requirement where the binary array being
    # searched must contain the same type as the element being searched for. Even with a custom sorting "key" to try to
    # map between the types on comparison, it won't allow it. Otherwise, the code below would probably work fine...
    #
    # end_marker = bwt_array[0].first_ch  # bwt_array[0] always has first_ch == end_marker because of lexicographic sort
    # found = 0
    # # Binary search the bwt_array for the left-most (top) entry with first_ch in its
    # bwt_top = bisect_left(
    #     bwt_array,
    #     test[-1],
    #     key=functools.cmp_to_key(lambda a, b: cmp(a.first_ch[0], b.first_ch[0], end_marker)))
    # if bwt_top == len(test):
    #     return 0  # not found
    # # Binary search the bwt_array for the right-most (bottom) entry with first_ch in its
    # bwt_bottom = bisect_right(
    #     bwt_array,
    #     test[-1],
    #     lo=bwt_top,
    #     key=functools.cmp_to_key(lambda a, b: cmp(a.first_ch[0], b.first_ch[0], end_marker)))
    # # If you're only searching for a single character, stop here.
    # if len(test) == 1:
    #     return bwt_bottom - bwt_top + 1
    # # Otherwise, scan only between those indices
    # for i in range(bwt_top, bwt_bottom + 1):
    #     rec = bwt_array[i]
    #     if rec.last_ch == test[-2] and walk_find(bwt_array, test, i):
    #         found += 1
    # return found
```