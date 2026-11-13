`{bm-disable-all}`[arithmetic_code/GreatestCommonDivisor.py](arithmetic_code/GreatestCommonDivisor.py) (lines 38 to 59):`{bm-enable-all}`

```python
@log_decorator
def gcd_factor(num1: int, num2: int) -> int:
    log(f'Calculating gcd for {num1} and {num2}...')
    log_indent()

    log(f'Calculating factors for {num1}...')
    factors1 = factor_fastest(num1)
    log(f'Factors for {num1}: {factors1}')

    log(f'Calculating factors for {num2}...')
    factors2 = factor_fastest(num2)
    log(f'Factors for {num2}: {factors2}')

    log(f'Finding common factors...')
    common_factors = factors1 & factors2  # set intersection
    log(f'Common factors for {num1} and {num2}: {common_factors}')

    found = max(common_factors)

    log_unindent()
    log(f'GCD is {found}')
    return found
```