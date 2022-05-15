`{bm-disable-all}`[ch9_code/src/sequence_search/SuffixArray.py](ch9_code/src/sequence_search/SuffixArray.py) (lines 96 to 117):`{bm-enable-all}`

```python
def has_prefix(
        prefix: StringView,
        end_marker: str,
        suffix_array: list[StringView]
) -> bool:
    assert end_marker not in prefix, f'{prefix} should not have end marker'
    start = 0
    end = len(suffix_array)
    while start != end:
        mid = (end - start) // 2
        mid_suffix = suffix_array[mid]
        comparison = cmp(prefix, mid_suffix)
        if common_prefix_len(prefix, mid_suffix) == len(prefix):
            return True
        elif comparison < 0:
            end = mid
        elif comparison > 0:
            start = mid
        else:
            raise ValueError('This should never happen')
    return False
```