import math
from sys import stdin

from Variance import population_variance


# MARKDOWN
def population_standard_deviation(data: list[float]) -> float:
    return math.sqrt(population_variance(data))

def sample_standard_deviation(data: list[float]) -> float:
    return math.sqrt(population_variance(data))
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
    sample_standard_deviation([3,4,5])
