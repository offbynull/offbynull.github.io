`{bm-disable-all}`[arithmetic_code/GreatestCommonDivisor.py](arithmetic_code/GreatestCommonDivisor.py) (lines 9 to 33):`{bm-enable-all}`

```python
@log_decorator
def gcd_naive(num1: WholeNumber, num2: WholeNumber) -> WholeNumber:
    log(f'Calculating gcd for {num1} and {num2}...')
    log_indent()

    log(f'Sorting to determine smaller input...')
    min_num = min(num1, num2)

    log(f'Testing up to smaller input ({min_num})...')
    log_indent()
    for i in WholeNumber.range(WholeNumber.from_str('1'), min_num, True):
        log(f'Testing {i}...')
        quotient1, remainder1 = num1 / i
        quotient2, remainder2 = num2 / i
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