```python
# Each index in object_repetitions represents a unique object, where the value at that index is the number of times that
# object repeats. For example, PEPPER may be represented as [1,3,1], where index ...
#  * 1 is the repetition count for E (2 time)
#  * 2 is the repetition count for P (3 times)
#  * 3 is the repetition count for R (1 time)
def count_permutations_with_repetitions(object_repetitions: list[int]) -> int:
    numerator = count_permutations(sum(object_repetitions))
    denominator = 1
    for repetitions in object_repetitions:
        denominator *= count_permutations(repetitions)
    return numerator // denominator
```