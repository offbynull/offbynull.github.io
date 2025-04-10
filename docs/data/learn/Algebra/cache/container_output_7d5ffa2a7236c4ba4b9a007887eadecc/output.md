`{bm-disable-all}`[arithmetic_code/LeastCommonMultiple.py](arithmetic_code/LeastCommonMultiple.py) (lines 10 to 39):`{bm-enable-all}`

```python
@log_decorator
def lcm_walk(num1: int, num2: int) -> tuple[list[int], list[int]]:
    num1_multiples: list[int] = []
    num2_multiples: list[int] = []

    num1_counter = 1
    num2_counter = 1

    while True:
        log(f'Calculating {num1_counter} multiple of {num1}...')
        num1_multiple = num1 * num1_counter
        num1_multiples.append(num1_multiple)

        log(f'Calculating {num2_counter} multiple of {num2}...')
        num2_multiple = num2 * num2_counter
        num2_multiples.append(num2_multiple)

        log(f'Testing {num1_multiple} vs {num2_multiple}')
        if num1_multiple == num2_multiple:
            log(f'Matches! LCM is {num1_multiple}')
            break
        elif num1_multiple < num2_multiple:
            log(f'Increasing first multiple (multiple for {num1})')
            num1_counter += 1
        elif num1_multiple > num2_multiple:
            log(f'Increasing second multiple (multiple for {num2})')
            num2_counter += 1

    return num1_multiple
```