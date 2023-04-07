```python
def count_combinations(n: int, r: int) -> int:
    if r < 0 or r > n:
        return 0
    elif r == n or r == 0:
        return 1
    return factorial(n) // (factorial(n-r) * factorial(r))
```