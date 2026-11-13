`{bm-disable-all}`[ch3_code/src/ReadPair.py](ch3_code/src/ReadPair.py) (lines 82 to 110):`{bm-enable-all}`

```python
def append_overlap(self: ReadPair, other: ReadPair, skip: int = 1) -> ReadPair:
    self_head = Read(self.data.head)
    other_head = Read(other.data.head)
    new_head = self_head.append_overlap(other_head)
    new_head = new_head.data

    self_tail = Read(self.data.tail)
    other_tail = Read(other.data.tail)
    new_tail = self_tail.append_overlap(other_tail)
    new_tail = new_tail.data

    # WARNING: new_d may go negative -- In the event of a negative d, it means that rather than there being a gap
    # in between the head and tail, there's an OVERLAP in between the head and tail. To get rid of the overlap, you
    # need to remove either the last d chars from head or first d chars from tail.
    new_d = self.d - skip
    kdmer = Kdmer(new_head, new_tail, new_d)

    return ReadPair(kdmer, source=('overlap', [self, other]))

@staticmethod
def stitch(items: List[ReadPair], skip: int = 1) -> str:
    assert len(items) > 0
    ret = items[0]
    for other in items[1:]:
        ret = ret.append_overlap(other, skip)
    assert ret.d <= 0, "Gap still exists -- not enough to stitch"
    overlap_count = -ret.d
    return ret.data.head + ret.data.tail[overlap_count:]
```