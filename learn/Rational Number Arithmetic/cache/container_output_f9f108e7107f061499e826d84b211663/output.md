`{bm-disable-all}`[arithmetic_code/DecimalNumber.py](arithmetic_code/DecimalNumber.py) (lines 111 to 169):`{bm-enable-all}`

```python
@staticmethod
@log_decorator
def to_suitable_fraction(value: FractionNumber) -> FractionNumber:
    log(f'Converting {value} to an equivalent fraction with denominator that is power of 10...')
    log_indent()

    denom = value.denominator

    if str(denom)[0] == '1' and (set(str(denom)[1:]) == set() or set(str(denom)[1:]) == set('0')):
        log(f'Already power of 10')
    else:
        log(f'No')
        log(f'Simplifying fraction {value}...')
        value = value.simplify()
        denom = value.denominator
        log(f'{value}')

        log(f'Calculating unique prime factors of {denom}...')
        denom_prime_factors = factor_tree(denom).get_prime_factors()
        denom_prime_factors_set = set(denom_prime_factors)
        log(f'{denom_prime_factors_set}')
        if not({WholeNumber.from_int(2), WholeNumber.from_int(5)} == denom_prime_factors_set
               or {WholeNumber.from_int(2)} == denom_prime_factors_set
               or {WholeNumber.from_int(5)} == denom_prime_factors_set
               or 0 == len(denom_prime_factors_set)):
            raise Exception('Simplified denominator contains prime factors other than 2 and 5')

        log(f'Calculating value to scale by so {denom} becomes next largest power of 10...')
        num_of_2s = len(list(filter(lambda pf: pf == WholeNumber.from_str('2'), denom_prime_factors)))
        num_of_5s = len(list(filter(lambda pf: pf == WholeNumber.from_str('5'), denom_prime_factors)))
        extra_2s = 0
        extra_5s = 0
        if num_of_2s == 0 and num_of_5s == 0:
            extra_2s = 1
            extra_5s = 1
        elif num_of_2s < num_of_5s:
            extra_2s = num_of_5s - num_of_2s
        elif num_of_2s > num_of_5s:
            extra_5s = num_of_2s - num_of_5s
        log(f'Require {extra_2s} 2s and {extra_5s} 5s')

        log(f'Multiplying {extra_2s} 2s and {extra_5s} 5s to get scale...')
        scale_by = WholeNumber.from_str('1')
        for i in range(extra_2s):
            scale_by *= WholeNumber.from_str('2')
        for i in range(extra_5s):
            scale_by *= WholeNumber.from_str('5')
        log(f'{scale_by}')

        log(f'Multiplying {value}\'s numerator and denominator by {scale_by}...')
        value = value * FractionNumber(
            IntegerNumber.from_whole(scale_by),
            IntegerNumber.from_whole(scale_by)
        )
        log(f'{value}')

    log_unindent()
    log(f'{value}')

    return value
```