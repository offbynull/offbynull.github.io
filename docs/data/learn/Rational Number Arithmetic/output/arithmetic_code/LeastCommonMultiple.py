from __future__ import annotations

from collections import Counter
from typing import List, Tuple, Set

from Factor import factor_tree
from Output import log_decorator, log
from WholeNumber import WholeNumber


#MARKDOWN_WALK
@log_decorator
def lcm_walk(num1: WholeNumber, num2: WholeNumber) -> Tuple[List[WholeNumber], List[WholeNumber]]:
    num1_multiples: List[WholeNumber] = []
    num2_multiples: List[WholeNumber] = []

    num1_counter = WholeNumber.from_int(1)
    num2_counter = WholeNumber.from_int(1)

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
            num1_counter += WholeNumber.from_int(1)
        elif num1_multiple > num2_multiple:
            log(f'Increasing second multiple (multiple for {num2})')
            num2_counter += WholeNumber.from_int(1)

    return num1_multiple
#MARKDOWN_WALK


#MARKDOWN_PF
@log_decorator
def lcm_prime_factorize(num1: WholeNumber, num2: WholeNumber) -> WholeNumber:
    log(f'Calculating prime factors for {num1}...')
    num1_primes = sorted(factor_tree(num1).get_prime_factors())
    log(f'{num1_primes}')

    log(f'Calculating prime factors for {num2}...')
    num2_primes = sorted(factor_tree(num2).get_prime_factors())
    log(f'{num2_primes}')

    distinct_primes: Set[WholeNumber] = set()
    [distinct_primes.add(p) for p in num1_primes]
    [distinct_primes.add(p) for p in num2_primes]

    log(f'Combining prime factors to get LCM...')
    least_common_multiple = WholeNumber.from_int(1)
    least_common_multiple_primes = Counter()
    for prime in sorted(list(distinct_primes)):
        num1_count = num1_primes.count(prime)
        num2_count = num2_primes.count(prime)
        if num1_count >= num2_count:
            for i in WholeNumber.range(WholeNumber.from_int(0), WholeNumber.from_int(num1_count)):
                least_common_multiple = least_common_multiple * prime
            least_common_multiple_primes[prime] += num1_count
        else:
            for i in WholeNumber.range(WholeNumber.from_int(0), WholeNumber.from_int(num2_count)):
                least_common_multiple = least_common_multiple * prime
            least_common_multiple_primes[prime] += num2_count
    log(f'LCM is {least_common_multiple}')

    return least_common_multiple
#MARKDOWN_PF


if __name__ == '__main__':
    print(f'{lcm_walk(WholeNumber.from_int(6), WholeNumber.from_int(7))}')
    print(f'{lcm_prime_factorize(WholeNumber.from_int(6), WholeNumber.from_int(7))}')