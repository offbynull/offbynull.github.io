def _fibonacci_number(last2, last1, stop_cnt, cnt):
    if cnt == stop_cnt:
        return last1
    return _fibonacci_number(last1, last1+last2, stop_cnt, cnt+1)


def fibonacci_number(cnt):
    if cnt <= 1:
        return cnt
    else:
        return _fibonacci_number(0, 1, cnt, 1)


for n in range(0,5):
    print(f'{n=} {fibonacci_number(n) % 5=} {fibonacci_number(n+1) % 5=}')
