```python
def count_grouped_permutations(n_list: list[int]) -> int:
    k = len(n_list)
    product = 1
    for n in n_list:
        product *= count_permutations(n)
    product *= k
    return product
```