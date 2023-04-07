from pathlib import Path
from sys import stdin
from typing import TypeVar

import yaml

from Frequency import frequency

T = TypeVar('T')


# MARKDOWN
def relative_frequency(data: list[T]) -> dict[T, int]:
    freqs = frequency(data)
    return {n: f / len(data) for n, f in freqs.items()}
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
    main()
