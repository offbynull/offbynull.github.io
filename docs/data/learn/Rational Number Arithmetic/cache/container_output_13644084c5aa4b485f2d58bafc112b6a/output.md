`{bm-disable-all}`[arithmetic_code/Factor.py](arithmetic_code/Factor.py) (lines 166 to 196):`{bm-enable-all}`

```python
@log_decorator
def ladder(num: WholeNumber) -> Set[WholeNumber]:
    prime_factors: List[WholeNumber] = []

    log(f'Testing primes (using ladder method) to see which is factor of {num}...')

    log_indent()
    while not is_prime(num):
        prime_to_test = WholeNumber.from_int(2)

        while True:
            log(f'Testing if {prime_to_test} is divisible by {num}...')
            (new_num, remainder) = num / prime_to_test
            if remainder == WholeNumber.from_int(0):
                break
            prime_to_test = calculate_next_prime(prime_to_test)

        log(f'Found! {prime_to_test} is a prime factor -- {new_num} * {prime_to_test} = {num}')
        prime_factors.append(prime_to_test)
        num = new_num

        log(f'Testing primes to see which is factor of {num}...')

    log(f'{num} itself is a prime!')
    prime_factors.append(num)

    log_unindent()
    log(f'Prime factors: {prime_factors}')

    return prime_factors
```