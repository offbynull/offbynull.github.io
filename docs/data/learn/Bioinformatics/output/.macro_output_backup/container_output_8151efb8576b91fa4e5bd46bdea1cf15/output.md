`{bm-disable-all}`[ch3_code/src/Read.py](ch3_code/src/Read.py) (lines 80 to 87):`{bm-enable-all}`

```python
# This is read breaking -- why not just call it break? because break is a reserved keyword.
def shatter(self: Read, k: int) -> List[Read]:
    ret = []
    for kmer, _ in slide_window(self.data, k):
        r = Read(kmer, source=('shatter', [self]))
        ret.append(r)
    return ret
```