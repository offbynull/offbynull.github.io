from pathlib import Path
from sys import stdin
from typing import TypeVar

import yaml

from Frequency import frequency
from RelativeFrequency import relative_frequency

T = TypeVar('T')


# MARKDOWN
def cumulative_frequency(data: list[T]) -> dict[T, int]:
    freqs = frequency(data)
    cum_freqs = {}
    last_val = 0
    for item in sorted(freqs):
        last_val += freqs[item]
        cum_freqs[item] = last_val
    return cum_freqs


def cumulative_relative_frequency(data: list[T]) -> dict[T, int]:
    freqs = relative_frequency(data)
    cum_freqs = {}
    last_val = 0
    for item in sorted(freqs):
        last_val += freqs[item]
        cum_freqs[item] = last_val
    return cum_freqs
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
