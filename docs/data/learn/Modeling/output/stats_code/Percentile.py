from bisect import bisect_left, bisect_right
from sys import stdin
from typing import TypeVar

T = TypeVar('T')


# MARKDOWN
def percentile_boundary(data: list[T], percent: float) -> float:
    data.sort()
    percentile_idx = percent * (len(data) - 1)
    return percentile_idx


def percentile_at(data: list[float], percent: float) -> float:
    percentile_idx = percentile_boundary(data, percent)
    if percentile_idx.is_integer():
        return data[int(percentile_idx)]
    elif len(data) > 1:  # Avg values in indexes to left and right (feels wishy-washy). More accurate ways available?
        prev_idx = int(percentile_idx)
        next_idx = prev_idx + 1
        return (data[prev_idx] + data[next_idx]) / 2
    else:
        return data[0]


def percentile_in(data: list[float], percent: float, test_val: float) -> bool:
    val = percentile_at(data, percent)
    return test_val <= val


def percentile_for(data: list[float], value: float) -> float:
    # Sort the data, then find out ...
    #   * how many elements come before value (before_cnt)
    #   * how many elements are value (cnt)
    # then calculate as (before_cnt + 0.5*cnt) / len. This came from the book and feels very wishy-washy. More accurate
    # ways available?
    data.sort()
    before_idx = bisect_left(data, value)
    if data[before_idx] == value:
        before_idx -= 1
    before_cnt = before_idx + 1
    cnt = 0
    at_idx = bisect_left(data, value)
    while at_idx < len(data) and data[at_idx] == value:
        cnt += 1
        at_idx += 1
    return (before_cnt + 0.5 * cnt) / len(data)
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
    percentile_for([1, 5, 4, 4, 5, 5, 6], 4.5)
