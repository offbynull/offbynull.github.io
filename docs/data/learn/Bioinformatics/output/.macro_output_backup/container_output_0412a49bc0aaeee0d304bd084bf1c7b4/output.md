`{bm-disable-all}`[ch7_code/src/phylogeny/TrimDistanceMatrix.py](ch7_code/src/phylogeny/TrimDistanceMatrix.py) (lines 13 to 28):`{bm-enable-all}`

```python
def trim(dm: DistanceMatrix, l: N) -> None:
    dm.delete(l)
    # The distance matrix's delete function handles row/column removal for a leaf node. It's
    # reproduced below to show what happens...
    #
    # def delete(self, id: N):
    #     if id not in self._keys:
    #         raise ValueError(f'{id} does not already exists')
    #     dels = []
    #     for i1, i2 in self._data.keys():
    #         if i1 == id or i2 == id:
    #             dels.append((i1, i2))
    #     for key in dels:
    #         del self._data[key]
    #     self._keys.remove(id)
```