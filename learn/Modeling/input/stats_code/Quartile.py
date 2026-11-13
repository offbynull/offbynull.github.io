from sys import stdin
from typing import TypeVar

from Percentile import percentile_at

T = TypeVar('T')


# MARKDOWN
def quartiles_at(data: list[T]) -> tuple[float, float, float]:
    return percentile_at(data, 0.25), \
        percentile_at(data, 0.5), \
        percentile_at(data, 0.75)
# MARKDOWN


# MARKDOWN_IQR
def iqr(data: list[float]) -> float:
    q1, _, q3 = quartiles_at(data)
    return q3 - q1
# MARKDOWN_IQR


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        data_raw = ''.join(stdin.readlines())
        print('```')
        exec(data_raw)
        print('```')
        print()
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()
