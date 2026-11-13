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


def fibonacci_last_digit(n):
    current, next = 0, 1
    for _ in range(n):
        current, next = next, (current + next) % 10

    return current


if __name__ == '__main__':
    n = int(input())
    print((fibonacci_last_digit((n + 2) % 60) + 9) % 10)
