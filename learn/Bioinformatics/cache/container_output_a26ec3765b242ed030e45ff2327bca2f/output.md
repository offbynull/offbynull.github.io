`{bm-disable-all}`[ch9_code/src/sequence_search/BurrowsWheelerTransform_Ranks.py](ch9_code/src/sequence_search/BurrowsWheelerTransform_Ranks.py) (lines 82 to 84):`{bm-enable-all}`

```python
def to_symbol_instance_count(rec: BWTRecord) -> int:
    ch = rec.last_ch
    return rec.last_tallies[ch]
```