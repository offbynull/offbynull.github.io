from __future__ import annotations


# MARKDOWN
def hamming_distance(kmer1: str, kmer2: str) -> int:
    mismatch = 0

    for ch1, ch2 in zip(kmer1, kmer2):
        if ch1 != ch2:
            mismatch += 1

    return mismatch
# MARKDOWN


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        kmer1 = input()
        kmer2 = input()
        hd = hamming_distance(kmer1, kmer2)
        print(f'Kmer1: {kmer1}\n')
        print(f'Kmer2: {kmer2}\n')
        print(f'Hamming Distance: {hd}')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()