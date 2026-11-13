`{bm-disable-all}`[ch9_code/src/sequence_search/SuffixArray.py](ch9_code/src/sequence_search/SuffixArray.py) (lines 90 to 131):`{bm-enable-all}`

```python
def find_prefix(
        prefix: StringView,
        end_marker: StringView,
        suffix_array: list[StringView]
) -> list[int]:
    assert end_marker not in prefix, f'{prefix} should not have end marker'
    # Binary search
    start = 0
    end = len(suffix_array) - 1
    found = None
    while start <= end:
        mid = start + ((end - start) // 2)
        mid_suffix = suffix_array[mid]
        comparison = cmp(prefix, mid_suffix, end_marker)
        if common_prefix_len(prefix, mid_suffix) == len(prefix):
            found = mid
            break
        elif comparison < 0:
            end = mid - 1
        elif comparison > 0:
            start = mid + 1
        else:
            raise ValueError('This should never happen')
    # If not found, return
    if found is None:
        return []
    # Walk backward to see how many before start with prefix
    start = found
    while start >= 0:
        start_suffix = suffix_array[start]
        if common_prefix_len(prefix, start_suffix) != len(prefix):
            break
        start -= 1
    # Walk forward to see how many after start with prefix
    end = found + 1
    while end < len(suffix_array):
        end_suffix = suffix_array[end]
        if common_prefix_len(prefix, end_suffix) != len(prefix):
            break
        end += 1
    return [sv.start for sv in suffix_array[start:end]]
```