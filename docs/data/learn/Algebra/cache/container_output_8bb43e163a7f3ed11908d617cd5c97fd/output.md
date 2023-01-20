`{bm-disable-all}`[arithmetic_code/GreatestCommonDivisor.py](arithmetic_code/GreatestCommonDivisor.py) (lines 64 to 87):`{bm-enable-all}`

```python
@log_decorator
def gcd_euclid(num1: int, num2: int) -> int:
    log(f'Calculating gcd for {num1} and {num2}...')
    log_indent()

    next_nums = [num1, num2]

    while True:
        log(f'Sorting {next_nums}...')
        next_nums.sort()  # sort smallest to largest
        next_nums.reverse()  # reverse it so that it's largest to largest
        log(f'Checking if finished ({next_nums[1]} == 0?)...')
        if next_nums[1] == 0:
            found = next_nums[0]
            break

        log(f'Dividing {next_nums} and grabbing the remainder for the next test...')
        _ = next_nums[0] // next_nums[1]
        remainder = next_nums[0] - (_ * next_nums[1])
        next_nums = [next_nums[1], remainder]

    log_unindent()
    log(f'GCD is {found}')
    return found
```