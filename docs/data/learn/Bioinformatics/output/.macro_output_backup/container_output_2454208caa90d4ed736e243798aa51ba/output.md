`{bm-disable-all}`[ch1_code/src/EstimateProbabilityOfKmerInArbitrarySequence.py](ch1_code/src/EstimateProbabilityOfKmerInArbitrarySequence.py) (lines 57 to 70):`{bm-enable-all}`

```python
def estimate_probability(searchspace_len: int, searchspace_symbol_count: int, search_for: List[int], min_occurrence: int) -> float:
    def factorial(num):
        if num == 1:
            return num
        else:
            return num * factorial(num - 1)

    def bc(m, k):
        return factorial(m) / (factorial(k) * factorial(m - k))

    k = len(search_for)
    n = (searchspace_len - min_occurrence * k)
    return bc(n + min_occurrence, min_occurrence) * (searchspace_symbol_count ** n) / searchspace_symbol_count ** searchspace_len
```