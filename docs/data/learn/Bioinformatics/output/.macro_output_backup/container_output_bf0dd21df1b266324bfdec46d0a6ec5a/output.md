`{bm-disable-all}`[ch1_code/src/ReverseComplementADnaKmer.py](ch1_code/src/ReverseComplementADnaKmer.py) (lines 5 to 22):`{bm-enable-all}`

```python
def reverse_complement(strand: str):
    ret = ''
    for i in range(0, len(strand)):
        base = strand[i]
        if base == 'A' or base == 'a':
            base = 'T'
        elif base == 'T' or base == 't':
            base = 'A'
        elif base == 'C' or base == 'c':
            base = 'G'
        elif base == 'G' or base == 'g':
            base = 'C'
        else:
            raise Exception('Unexpected base: ' + base)

        ret += base
    return ret[::-1]
```