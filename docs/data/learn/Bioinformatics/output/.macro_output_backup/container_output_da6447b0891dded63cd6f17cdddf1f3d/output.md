`{bm-disable-all}`[ch5_code/src/global_alignment/Global_SweepCombiner.py](ch5_code/src/global_alignment/Global_SweepCombiner.py) (lines 10 to 19):`{bm-enable-all}`

```python
class SweepCombiner:
    def __init__(self, v: List[ELEM], w: List[ELEM], weight_lookup: WeightLookup):
        self.forward_sweeper = ForwardSweeper(v, w, weight_lookup)
        self.reverse_sweeper = ReverseSweeper(v, w, weight_lookup)

    def get_col(self, idx: int):
        fcol = self.forward_sweeper.get_col(idx)
        rcol = self.reverse_sweeper.get_col(idx)
        return [a + b for a, b in zip(fcol, rcol)]
```