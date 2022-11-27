def fibonacci_last_digit(n):
    current, next = 0, 1
    for _ in range(n):
        current, next = next, (current + next) % 10

    return current


def sum_last_digit(n):
    return (fibonacci_last_digit((n + 2) % 60) + 9) % 10


if __name__ == '__main__':
    m, n = map(int, input().split())
    print((sum_last_digit(n) - sum_last_digit(m - 1)) % 10)