`{bm-disable-all}`[ch3_code/src/ToOverlapGraphHash.py](ch3_code/src/ToOverlapGraphHash.py) (lines 13 to 36):`{bm-enable-all}`

```python
def to_overlap_graph(items: List[T], skip: int = 1) -> Graph[T]:
    ret = Graph()

    prefixes = dict()
    suffixes = dict()
    for i, item in enumerate(items):
        prefix = item.prefix(skip)
        prefixes.setdefault(prefix, set()).add(i)
        suffix = item.suffix(skip)
        suffixes.setdefault(suffix, set()).add(i)

    for key, indexes in suffixes.items():
        other_indexes = prefixes.get(key)
        if other_indexes is None:
            continue
        for i in indexes:
            item = items[i]
            for j in other_indexes:
                if i == j:
                    continue
                other_item = items[j]
                ret.insert_edge(item, other_item)
    return ret
```