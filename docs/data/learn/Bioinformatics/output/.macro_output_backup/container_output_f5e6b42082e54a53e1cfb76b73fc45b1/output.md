`{bm-disable-all}`[ch3_code/src/ReadPair.py](ch3_code/src/ReadPair.py) (lines 113 to 124):`{bm-enable-all}`

```python
# This is read breaking -- why not just call it break? because break is a reserved keyword.
def shatter(self: ReadPair, k: int) -> List[ReadPair]:
    ret = []
    d = (self.k - k) + self.d
    for window_head, window_tail in zip(slide_window(self.data.head, k), slide_window(self.data.tail, k)):
        kmer_head, _ = window_head
        kmer_tail, _ = window_tail
        kdmer = Kdmer(kmer_head, kmer_tail, d)
        rp = ReadPair(kdmer, source=('shatter', [self]))
        ret.append(rp)
    return ret
```