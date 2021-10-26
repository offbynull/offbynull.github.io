`{bm-disable-all}`[ch5_code/src/scoring/SumOfPairsWeightLookup.py](ch5_code/src/scoring/SumOfPairsWeightLookup.py) (lines 8 to 14):`{bm-enable-all}`

```python
class SumOfPairsWeightLookup(WeightLookup):
    def __init__(self, backing_2d_lookup: WeightLookup):
        self.backing_wl = backing_2d_lookup

    def lookup(self, *elements: Tuple[Optional[ELEM], ...]):
        return sum(self.backing_wl.lookup(a, b) for a, b in combinations(elements, r=2))
```