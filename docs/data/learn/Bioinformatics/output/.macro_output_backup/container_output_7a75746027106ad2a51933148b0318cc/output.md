`{bm-disable-all}`[ch5_code/src/scoring/EntropyWeightLookup.py](ch5_code/src/scoring/EntropyWeightLookup.py) (lines 9 to 31):`{bm-enable-all}`

```python
class EntropyWeightLookup(WeightLookup):
    def __init__(self, indel_weight: float):
        self.indel_weight = indel_weight

    @staticmethod
    def _calculate_entropy(values: Tuple[float, ...]) -> float:
        ret = 0.0
        for value in values:
            ret += value * (log(value, 2.0) if value > 0.0 else 0.0)
        ret = -ret
        return ret

    def lookup(self, *elements: Tuple[Optional[ELEM], ...]):
        if None in elements:
            return self.indel_weight

        counts = Counter(elements)
        total = len(elements)
        probs = tuple(v / total for k, v in counts.most_common())
        entropy = EntropyWeightLookup._calculate_entropy(probs)

        return -entropy
```