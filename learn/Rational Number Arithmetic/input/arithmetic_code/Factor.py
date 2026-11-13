from __future__ import annotations
from typing import Set, Tuple, List, Optional

from Output import log_indent, log_unindent, log, log_decorator
from WholeNumber import WholeNumber

#MARKDOWN_NAIVE
@log_decorator
def factor_naive(num: WholeNumber) -> Set[WholeNumber]:
    log(f'Factoring {num}...')
    log_indent()

    factors: Set[WholeNumber] = set()
    for factor1 in WholeNumber.range(WholeNumber.from_int(1), num, end_inclusive=True):
        for factor2 in WholeNumber.range(WholeNumber.from_int(1), num, end_inclusive=True):
            log(f'Testing if {factor1} and {factor2} are factors...')
            if factor1 * factor2 == num:
                factors.add(factor1)
                factors.add(factor2)
                log(f'Yes')
            else:
                log(f'No')

    log_unindent()
    log(f'{factors}')

    return factors
#MARKDOWN_NAIVE


#MARKDOWN_FAST
@log_decorator
def factor_fast(num: WholeNumber) -> Set[WholeNumber]:
    log(f'Factoring {num}...')
    log_indent()

    factors: Set[WholeNumber] = set()
    for factor1 in WholeNumber.range(WholeNumber.from_int(1), num, end_inclusive=True):
        log(f'Test if {factor1} is a factor...')
        factor2, remainder = num / factor1
        if remainder == WholeNumber.from_int(0):
            factors.add(factor1)
            factors.add(factor2)
            log(f'Yes: ({factor1} and {factor2} are factors)')
        else:
            log(f'No')

    log_unindent()
    log(f'{factors}')

    return factors
#MARKDOWN_FAST


#MARKDOWN_FASTEST
@log_decorator
def factor_fastest(num: WholeNumber) -> Set[WholeNumber]:
    log(f'Factoring {num}...')
    log_indent()

    factors: Set[WholeNumber] = set()
    for factor1 in WholeNumber.range(WholeNumber.from_int(1), num, end_inclusive=True):
        log(f'Test if {factor1} is a factor...')
        factor2, remainder = num / factor1
        if remainder == WholeNumber.from_int(0):
            factors.add(factor1)
            factors.add(factor2)
            log(f'Yes: ({factor1} and {factor2} are factors)')
        else:
            log(f'No')

        if factor2 <= factor1:
            break

    log_unindent()
    log(f'{factors}')

    return factors
#MARKDOWN_FASTEST


#MARKDOWN_PRIMETEST
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
#MARKDOWN_PRIMETEST


#MARKDOWN_FACTORTREE
@log_decorator
def factor_tree(num: WholeNumber) -> FactorTreeNode:
    log(f'Creating factor tree for {num}...')

    factors = factor_fastest(num)

    # remove factor pairs that can't used in factor true: (1, num) or (num, 1)
    factors = set([f for f in factors if f != WholeNumber.from_int(1) and f != num])

    ret = FactorTreeNode()
    if len(factors) == 0:
        ret.value = num
        log(f'Cannot factor {num} is prime -- resulting tree: {ret}')
    else:
        factor1 = next(iter(factors))
        factor2, _ = num / factor1
        ret.value = num
        ret.left = factor_tree(factor1)
        ret.right = factor_tree(factor2)
        log(f'Factored {num} to {factor1} and {factor2} -- resulting tree: {ret}')
    return ret
#MARKDOWN_FACTORTREE


class FactorTreeNode:
    value: WholeNumber
    left: Optional[FactorTreeNode]
    right: Optional[FactorTreeNode]

    def __init__(self):
        self.left = None
        self.right = None

    def get_prime_factors(self, output_list: List[WholeNumber] = None) -> List[WholeNumber]:
        if output_list is None:
            output_list = []

        if self.left is None and self.right is None:
            if self.value != WholeNumber.from_str('1'):  # REMEMBER: 1 is not a prime number
                output_list.append(self.value)

        if self.left is not None:
            self.left.get_prime_factors(output_list)
        if self.right is not None:
            self.right.get_prime_factors(output_list)

        return output_list

    def __str__(self):
        ret = str(self.value)
        if self.left is not None and self.right is not None:
            ret += '('
            if self.left is not None:
                ret += str(self.left)
            ret += ','
            if self.right is not None:
                ret += str(self.right)
            ret += ')'
        return ret


#MARKDOWN_LADDER
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
#MARKDOWN_LADDER


def calculate_next_prime(last_prime: WholeNumber) -> WholeNumber:
    next_possible_prime = last_prime + WholeNumber.from_int(1)
    while True:
        if is_prime(next_possible_prime):
            return next_possible_prime
        else:
            next_possible_prime += WholeNumber.from_int(1)




if __name__ == '__main__':
    # factors = factor_naive(WholeNumber(24))
    # factors = factor_fast(WholeNumber(24))
    # factors = factor_fastest(WholeNumber(24))
    # print(f'{factors}')
    # print(f'{prime_test(WholeNumber(49))}')
    tree = factor_tree(WholeNumber.from_int(24))
    print(f'{tree}')
    # print(f'{ladder(WholeNumber(24))}')