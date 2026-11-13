from statistics import mean
from sys import stdin

from Deviation import deviation


# MARKDOWN
def population_variance(data: list[float]) -> float:
    sq_devs = [deviation(data, i)**2 for i in range(len(data))]
    return mean(sq_devs)

def sample_variance(data: list[float]) -> float:
    sq_devs = [deviation(data, i)**2 for i in range(len(data))]
    return sum(sq_devs) / (len(data) - 1)
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
    sample_variance([3,4,5])
