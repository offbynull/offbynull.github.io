`{bm-disable-all}`[ch1_code/src/GCSkew.py](ch1_code/src/GCSkew.py) (lines 8 to 21):`{bm-enable-all}`

```python
def gc_skew(seq: str):
    counter = 0
    skew = [counter]
    for i in range(len(seq)):
        if seq[i] == 'G':
            counter += 1
            skew.append(counter)
        elif seq[i] == 'C':
            counter -= 1
            skew.append(counter)
        else:
            skew.append(counter)
    return skew
```