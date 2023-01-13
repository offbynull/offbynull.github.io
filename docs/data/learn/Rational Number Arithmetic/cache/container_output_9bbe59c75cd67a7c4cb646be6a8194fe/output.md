`{bm-disable-all}`[arithmetic_code/GreatestCommonDivisor.py](arithmetic_code/GreatestCommonDivisor.py) (lines 63 to 85):`{bm-enable-all}`

```python
@log_decorator
def gcd_euclid(num1: WholeNumber, num2: WholeNumber) -> WholeNumber:
    log(f'Calculating gcd for {num1} and {num2}...')
    log_indent()

    next_nums = [num1, num2]

    while True:
        log(f'Sorting {next_nums}...')
        next_nums.sort()  # sort smallest to largest
        next_nums.reverse()  # reverse it so that it's largest to largest
        log(f'Checking if finished ({next_nums[1]} == 0?)...')
        if next_nums[1] == WholeNumber.from_int(0):
            found = next_nums[0]
            break

        log(f'Dividing {next_nums} and grabbing the remainder for the next test...')
        _, remainder = next_nums[0] / next_nums[1]
        next_nums = [next_nums[1], remainder]

    log_unindent()
    log(f'GCD is {found}')
    return found
```