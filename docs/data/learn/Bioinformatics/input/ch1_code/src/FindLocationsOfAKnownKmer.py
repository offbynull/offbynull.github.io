from __future__ import annotations

from typing import List


# MARKDOWN
def find_kmer_locations(sequence: str, kmer: str) -> List[int]:
    k = len(kmer)
    idxes = []
    for i in range(0, len(sequence) - k + 1):
        if sequence[i:i + k] == kmer:
            idxes.append(i)
    return idxes
# MARKDOWN


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        seq = input()
        kmer = input()
        idxes = find_kmer_locations(seq, kmer)
        print(f'Found {kmer} in {seq} at index {idxes}')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()