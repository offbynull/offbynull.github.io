`{bm-disable-all}`[ch3_code/src/FragmentOccurrenceProbabilityCalculator.py](ch3_code/src/FragmentOccurrenceProbabilityCalculator.py) (lines 15 to 29):`{bm-enable-all}`

```python
# If less than 50% of the reads are from repeats, this attempts to count and normalize such that it can hint at which
# reads may contain errors (= ~0) and which reads are for repeat regions (> 1.0).
def calculate_fragment_occurrence_probabilities(fragments: List[T]) -> Dict[T, float]:
    counter = Counter(fragments)
    max_digit_count = max([len(str(count)) for count in counter.values()])
    for i in range(max_digit_count):
        rounded_counter = Counter(dict([(k, round(count, -i)) for k, count in counter.items()]))
        for k, orig_count in counter.items():
            if rounded_counter[k] == 0:
                rounded_counter[k] = orig_count
        most_occurring_count, times_counted = Counter(rounded_counter.values()).most_common(1)[0]
        if times_counted >= len(rounded_counter) * 0.5:
            return dict([(key, value / most_occurring_count) for key, value in rounded_counter.items()])
    raise ValueError(f'Failed to find a common count: {counter}')
```