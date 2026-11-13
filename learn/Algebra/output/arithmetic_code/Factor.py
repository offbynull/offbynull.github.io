from __future__ import annotations

from Output import log_indent, log_unindent, log, log_decorator

#MARKDOWN_NAIVE
@log_decorator
def factor_naive(num: int) -> set[int]:
    log(f'Factoring {num}...')
    log_indent()

    factors: set[int] = set()
    for factor1 in range(1, num+1):
        for factor2 in range(1, num+1):
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
def factor_fast(num: int) -> set[int]:
    log(f'Factoring {num}...')
    log_indent()

    factors: set[int] = set()
    for factor1 in range(1, num+1):
        log(f'Test if {factor1} is a factor...')
        factor2 = num // factor1
        remainder = num - (factor1 * factor2)
        if remainder == 0:
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
def factor_fastest(num: int) -> set[int]:
    log(f'Factoring {num}...')
    log_indent()

    factors: set[int] = set()
    for factor1 in range(1, num+1):
        log(f'Test if {factor1} is a factor...')
        factor2 = num // factor1
        remainder = num - (factor1 * factor2)
        if remainder == 0:
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
def is_prime(num: int) -> bool:
    log(f'Test if {num} is prime...')
    log_indent()

    num_factors = factor_fastest(num)

    # At a minimum, all counting numbers have the factors 1 and the number itself (2 factors). If
    # there are more factore than that, it's a composite. Otherwise, it's a primse.

    log_unindent()
    if len(num_factors) == 2:
        log(f'{num}\'s factors are {num_factors} -- it is a prime')
        return True
    else:
        log(f'{num}\'s factors are {num_factors} -- it is a composite')
        return False
#MARKDOWN_PRIMETEST


#MARKDOWN_FACTORTREE
@log_decorator
def factor_tree(num: int) -> FactorTreeNode:
    log(f'Creating factor tree for {num}...')

    factors = factor_fastest(num)

    # remove factor pairs that can't used in factor true: (1, num) or (num, 1)
    factors = set([f for f in factors if f != 1 and f != num])

    ret = FactorTreeNode()
    if len(factors) == 0:
        ret.value = num
        log(f'Cannot factor {num} is prime -- resulting tree: {ret}')
    else:
        factor1 = next(iter(factors))
        factor2 = num // factor1
        ret.value = num
        ret.left = factor_tree(factor1)
        ret.right = factor_tree(factor2)
        log(f'Factored {num} to {factor1} and {factor2} -- resulting tree: {ret}')
    return ret
#MARKDOWN_FACTORTREE


class FactorTreeNode:
    value: int
    left: FactorTreeNode | None
    right: FactorTreeNode | None

    def __init__(self):
        self.left = None
        self.right = None

    def get_prime_factors(self, output_list: list[int] = None) -> list[int]:
        if output_list is None:
            output_list = []

        if self.left is None and self.right is None:
            if self.value != 1:  # REMEMBER: 1 is not a prime number
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
def ladder(num: int) -> list[int]:
    prime_factors: list[int] = []

    log(f'Testing primes (using ladder method) to see which is factor of {num}...')

    log_indent()
    while not is_prime(num):
        prime_to_test = 2

        while True:
            log(f'Testing if {prime_to_test} is divisible by {num}...')
            new_num = num // prime_to_test
            remainder = num - (new_num * prime_to_test)
            if remainder == 0:
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


def calculate_next_prime(last_prime: int) -> int:
    next_possible_prime = last_prime + 1
    while True:
        if is_prime(next_possible_prime):
            return next_possible_prime
        else:
            next_possible_prime += 1




if __name__ == '__main__':
    # factors = factor_naive(int(24))
    # factors = factor_fast(int(24))
    # factors = factor_fastest(int(24))
    # print(f'{factors}')
    # print(f'{prime_test(int(49))}')
    tree = factor_tree(24)
    print(f'{tree}')
    # print(f'{ladder(int(24))}')