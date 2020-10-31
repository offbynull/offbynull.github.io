from __future__ import annotations


# MARKDOWN
def find_all_dna_kmers_within_hamming_distance(kmer: str, hamming_dist: int) -> set[str]:
    def recurse(kmer: str, hamming_dist: int, output: set[str]) -> None:
        if hamming_dist == 0:
            output.add(kmer)
            return

        for i in range(0, len(kmer)):
            for ch in 'ACTG':
                neighbouring_kmer = kmer[:i] + ch + kmer[i + 1:]
                recurse(neighbouring_kmer, hamming_dist - 1, output)

    output = set()
    recurse(kmer, hamming_dist, output)

    return output
# MARKDOWN


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        kmer = input()
        min_hamming_dist = int(input())
        neighborhood = find_all_dna_kmers_within_hamming_distance(kmer, min_hamming_dist)
        print(f'Kmers within hamming distance {min_hamming_dist} of {kmer}: {neighborhood}')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()