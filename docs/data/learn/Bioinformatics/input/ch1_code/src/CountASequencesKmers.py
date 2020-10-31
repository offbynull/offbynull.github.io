from __future__ import annotations

from collections import Counter


# MARKDOWN
def kmer_frequency(data: str, k: int) -> Counter[str]:
    counter = Counter()
    for i in range(0, len(data) - k + 1):
        pattern = data[i:i+k]
        counter[pattern] += 1
    return counter
# MARKDOWN


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        seq = input()
        k = int(input())
        counts = kmer_frequency(seq, k)
        print(f'{k}-mer frequencies for {seq}:')
        [print(f' * {key} = {value}') for key, value in counts.items()]
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()