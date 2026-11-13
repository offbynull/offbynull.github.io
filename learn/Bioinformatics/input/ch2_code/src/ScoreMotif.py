from collections import Counter
from typing import List


# This function scores a motif by summing up the number of UNPOPULAR items in a column. For example, imagine a column
# has 7 Ts, 2 Cs, and 1A. The Ts are the most popular (7 items), meaning that the 3 items (2 Cs and 1 A) are unpopular
# -- the score for the column is 3.
#
# Sum up each of the column scores to the get the final score for the motif matrix.
#
# According to the book, this method of scoring a motif matrix isn't the method used in the real-world. The method used
# in the real-world is the one defined in MotifyEntropy.py, where...
# 1. each column has its probability distribution calculated (prob of A vs prob C vs prob of T vs prob of G)
# 2. the entropy of each of those prob dist are calculated
# 3. those entropies are summed up to get the entropy of the motif
# MARKDOWN
def score_motif(motif_matrix: List[str]) -> int:
    rows = len(motif_matrix)
    cols = len(motif_matrix[0])

    # count up each column
    counter_per_col = []
    for c in range(0, cols):
        counter = Counter()
        for r in range(0, rows):
            counter[motif_matrix[r][c]] += 1
        counter_per_col.append(counter)

    # sum counts for each column AFTER removing the top-most count -- that is, consider the top-most count as the
    # most popular char, so you're summing the counts of all the UNPOPULAR chars
    unpopular_sums = []
    for counter in counter_per_col:
        most_popular_item = counter.most_common(1)[0][0]
        del counter[most_popular_item]
        unpopular_sum = sum(counter.values())
        unpopular_sums.append(unpopular_sum)

    return sum(unpopular_sums)
# MARKDOWN


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        dnas = []
        while True:
            try:
                dna = input().strip().upper()
                if len(dna) > 0:
                    dnas.append(dna)
            except EOFError:
                break

        score = score_motif(dnas)
        print(f'Scoring...\n\n')
        print(f'{"<br>".join(dnas)}\n\n')
        print(f'{score}\n\n')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()