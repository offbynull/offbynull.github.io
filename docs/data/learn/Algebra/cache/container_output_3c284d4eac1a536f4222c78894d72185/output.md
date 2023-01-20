`{bm-disable-all}`[arithmetic_code/LeastCommonMultiple.py](arithmetic_code/LeastCommonMultiple.py) (lines 43 to 74):`{bm-enable-all}`

```python
@log_decorator
def lcm_prime_factorize(num1: int, num2: int) -> int:
    log(f'Calculating prime factors for {num1}...')
    num1_primes = sorted(factor_tree(num1).get_prime_factors())
    log(f'{num1_primes}')

    log(f'Calculating prime factors for {num2}...')
    num2_primes = sorted(factor_tree(num2).get_prime_factors())
    log(f'{num2_primes}')

    distinct_primes: set[int] = set()
    [distinct_primes.add(p) for p in num1_primes]
    [distinct_primes.add(p) for p in num2_primes]

    log(f'Combining prime factors to get LCM...')
    least_common_multiple = 1
    least_common_multiple_primes = Counter()
    for prime in sorted(list(distinct_primes)):
        num1_count = num1_primes.count(prime)
        num2_count = num2_primes.count(prime)
        if num1_count >= num2_count:
            for i in range(0, num1_count):
                least_common_multiple = least_common_multiple * prime
            least_common_multiple_primes[prime] += num1_count
        else:
            for i in range(0, num2_count):
                least_common_multiple = least_common_multiple * prime
            least_common_multiple_primes[prime] += num2_count
    log(f'LCM is {least_common_multiple}')

    return least_common_multiple
```