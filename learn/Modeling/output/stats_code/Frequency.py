from pathlib import Path
from sys import stdin
from typing import TypeVar

import yaml

T = TypeVar('T')


# MARKDOWN
def frequency(data: list[T]) -> dict[T, int]:
    ret = {}
    for v in data:
        v_freq = ret.get(v, 0) + 1
        ret[v] = v_freq
    return ret
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
