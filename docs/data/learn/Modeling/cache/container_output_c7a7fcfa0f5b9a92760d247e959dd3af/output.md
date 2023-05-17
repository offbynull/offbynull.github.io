```python
def count_combinations_via_pascal_recurrence(n: int, r: int) -> int:
    if n == 0:
        return 1
    if r == 0 or r == n:
        return 1
    return count_combinations_via_pascal_recurrence(n - 1, r - 1)\
        + count_combinations_via_pascal_recurrence(n - 1, r)
```