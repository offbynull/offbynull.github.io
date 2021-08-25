`{bm-disable-all}`[ch1_code/src/HammingDistanceBetweenKmers.py](ch1_code/src/HammingDistanceBetweenKmers.py) (lines 5 to 13):`{bm-enable-all}`

```python
def hamming_distance(kmer1: str, kmer2: str) -> int:
    mismatch = 0

    for ch1, ch2 in zip(kmer1, kmer2):
        if ch1 != ch2:
            mismatch += 1

    return mismatch
```