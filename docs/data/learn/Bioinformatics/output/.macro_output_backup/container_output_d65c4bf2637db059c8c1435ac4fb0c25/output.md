`{bm-disable-all}`[ch3_code/src/Read.py](ch3_code/src/Read.py) (lines 55 to 76):`{bm-enable-all}`

```python
def append_overlap(self: Read, other: Read, skip: int = 1) -> Read:
    offset = len(self.data) - len(other.data)
    data_head = self.data[:offset]
    data = self.data[offset:]

    prefix = data[:skip]
    overlap1 = data[skip:]
    overlap2 = other.data[:-skip]
    suffix = other.data[-skip:]
    ret = data_head + prefix
    for ch1, ch2 in zip(overlap1, overlap2):
        ret += ch1 if ch1 == ch2 else '?'  # for failure, use IUPAC nucleotide codes instead of question mark?
    ret += suffix
    return Read(ret, source=('overlap', [self, other]))

@staticmethod
def stitch(items: List[Read], skip: int = 1) -> str:
    assert len(items) > 0
    ret = items[0]
    for other in items[1:]:
        ret = ret.append_overlap(other, skip)
    return ret.data
```