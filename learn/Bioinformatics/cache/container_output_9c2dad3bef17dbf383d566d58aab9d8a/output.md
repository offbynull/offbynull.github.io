`{bm-disable-all}`[ch2_code/src/ConsensusString.py](ch2_code/src/ConsensusString.py) (lines 5 to 15):`{bm-enable-all}`

```python
def get_consensus_string(kmers: List[str]) -> str:
    count = len(kmers[0]);
    out = ''
    for i in range(0, count):
        c = Counter()
        for kmer in kmers:
            c[kmer[i]] += 1
        ch = c.most_common(1)
        out += ch[0][0]
    return out
```