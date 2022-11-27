def pisano_period(m):
    current = 0
    next = 1
    period = 0
    while True:
        old_next = next
        next = (current + next) % m
        current = old_next
        period = period + 1
        if current == 0 and next == 1:
            return period


def fibonacci(n):
    if n <= 1:
        return n

    previous = 0
    current = 1

    for _ in range(n - 1):
        previous, current = current, (previous + current)

    return current


if __name__ == '__main__':
    # print(f'{pisano_period(5)}')
    n, m = map(int, input().split())
    n = n % pisano_period(m)
    print(fibonacci(n) % m)