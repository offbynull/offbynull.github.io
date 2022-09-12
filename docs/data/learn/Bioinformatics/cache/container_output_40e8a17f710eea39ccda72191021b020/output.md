`{bm-disable-all}`[ch9_code/src/sequence_search/BurrowsWheelerTransform_CollapsedFirst.py](ch9_code/src/sequence_search/BurrowsWheelerTransform_CollapsedFirst.py) (lines 85 to 91):`{bm-enable-all}`

```python
def to_first_index(
        bwt_first_occurrence_map: dict[str, int],
        symbol_instance: tuple[str, int]
) -> int:
    symbol, symbol_count = symbol_instance
    return bwt_first_occurrence_map[symbol] + symbol_count - 1
```