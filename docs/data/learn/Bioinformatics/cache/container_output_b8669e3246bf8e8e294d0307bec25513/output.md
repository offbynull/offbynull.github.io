`{bm-disable-all}`[ch9_code/src/sequence_search/BurrowsWheelerTransform_CollapsedFirst.py](ch9_code/src/sequence_search/BurrowsWheelerTransform_CollapsedFirst.py) (lines 94 to 100):`{bm-enable-all}`

```python
# This is just a wrapper for to_first_row(). It's here for clarity.
def last_to_first(
        bwt_first_occurrence_map: dict[str, int],
        symbol_instance: tuple[str, int]
) -> int:
    return to_first_row(bwt_first_occurrence_map, symbol_instance)
```