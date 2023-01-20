`{bm-disable-all}`[arithmetic_code/GreatestCommonDivisor.py](arithmetic_code/GreatestCommonDivisor.py) (lines 8 to 34):`{bm-enable-all}`

```python
@log_decorator
def gcd_naive(num1: int, num2: int) -> int:
    log(f'Calculating gcd for {num1} and {num2}...')
    log_indent()

    log(f'Sorting to determine smaller input...')
    min_num = min(num1, num2)

    log(f'Testing up to smaller input ({min_num})...')
    log_indent()
    for i in range(1, min_num+1):
        log(f'Testing {i}...')
        quotient1 = num1 // i
        remainder1 = num1 - (i * quotient1)
        quotient2 = num2 // i
        remainder2 = num2 - (i * quotient2)
        if remainder1 == 0 and remainder2 == 0:
            log(f'{num1} and {num2} are both divisible by {i}...')
            found = i
        else:
            log(f'{num1} and {num2} are NOT both divisible by {i}...')
    log_unindent()

    log_unindent()
    log(f'GCD is {found}')
    return found
```