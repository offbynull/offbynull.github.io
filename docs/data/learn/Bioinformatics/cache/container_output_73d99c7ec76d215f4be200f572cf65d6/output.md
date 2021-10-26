`{bm-disable-all}`[ch1_code/src/BruteforceProbabilityOfKmerInArbitrarySequence.py](ch1_code/src/BruteforceProbabilityOfKmerInArbitrarySequence.py) (lines 9 to 39):`{bm-enable-all}`

```python
# Of the X sequence combinations tried, Y had the k-mer. The probability is Y/X.
def bruteforce_probability(searchspace_len: int, searchspace_symbol_count: int, search_for: List[int], min_occurrence: int) -> (int, int):
    found = 0
    found_max = searchspace_symbol_count ** searchspace_len

    str_to_search = [0] * searchspace_len

    def count_instances():
        ret = 0
        for i in range(0, searchspace_len - len(search_for) + 1):
            if str_to_search[i:i + len(search_for)] == search_for:
                ret += 1
        return ret

    def walk(idx: int):
        nonlocal found

        if idx == searchspace_len:
            count = count_instances()
            if count >= min_occurrence:
                found += 1
        else:
            for i in range(0, searchspace_symbol_count):
                walk(idx + 1)
                str_to_search[idx] += 1
            str_to_search[idx] = 0

    walk(0)

    return found, found_max
```