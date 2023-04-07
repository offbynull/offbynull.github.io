```python
def count_combinations_with_exclude_restrictions(n: int, r: int, exclude_object_count: int) -> int:
    return count_combinations(n, r) - count_combinations_with_include_restrictions(n, r, exclude_object_count)
```