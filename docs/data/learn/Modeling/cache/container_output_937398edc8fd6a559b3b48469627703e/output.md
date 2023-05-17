```python
def count_combinations_with_include_restrictions(n: int, r: int, include_object_count: int) -> int:
    return count_combinations(n - include_object_count, r - include_object_count)
```