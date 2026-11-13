`{bm-disable-all}`[arithmetic_code/Factor.py](arithmetic_code/Factor.py) (lines 83 to 100):`{bm-enable-all}`

```python
@log_decorator
def is_prime(num: WholeNumber) -> bool:
    log(f'Test if {num} is prime...')
    log_indent()

    num_factors = factor_fastest(num)

    # At a minimum, all counting numbers have the factors 1 and the number itself (2 factors). If
    # there are more factore than that, it's a composite. Otherwise, it's a primse.

    log_unindent()
    if len(num_factors) == 2:
        log(f'{num}\'s factors are {num_factors} -- it is a prime');
        return True
    else:
        log(f'{num}\'s factors are {num_factors} -- it is a composite');
        return False
```