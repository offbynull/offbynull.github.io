from sys import stdin
from typing import TypeVar

from Percentile import percentile_at

T = TypeVar('T')


# MARKDOWN
def mean(data: list[float]) -> float:
    return sum(data) / len(data)
# MARKDOWN


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
    mean([3,4,5])