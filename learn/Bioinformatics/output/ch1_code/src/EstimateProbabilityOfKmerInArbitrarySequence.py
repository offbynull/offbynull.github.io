from typing import List


# The explanation in the comments below are a bastardization of "1.13 Detour: Probabilities of Patterns in a String"
# in the Pevzner book...
#
# This implementation tries estimating the probability by ignoring the fact that the occurrences of a k-mer in a
# sequence may overlap. For example, searching for the 2-mer AA in the sequence AAAT yields 2 instances of AA:
#
# * [AA]AT
# * A[AA]T
#
# If we go ahead and ignore overlaps, we can think of the k-mers occurring in a string as insertions. For example,
# imagine a sequence of length 7 and the 2-mer AA. If we were to inject 2 instances of AA into the sequence to get it
# to reach length 7, how would that look?
#
# 2 instances of a 2-mer is 4 characters has a length of 5. To get the sequence to end up with a length of 7 after the
# insertions, the sequence needs to start with a length of 3:
#
# SSS
#
# Given that we're changing reality to say that the instances WON'T overlap in the sequence, we can treat each
# instance of the 2-mer AA as a single entity being inserted. The number of ways that these 2 instances can be inserted
# into the sequence is 10:
#
# I = insertion of AA, S = arbitrary sequence character
#
# IISSS  ISISS  ISSIS  ISSSI
# SIISS  SISIS  SISSI
# SSIIS  SSISI
# SSSII
#
# Another way to think of the above insertions is that they aren't insertions. Rather, we have 5 items in total and
# we're selecting 2 of them. How many ways can we select 2 of those 5 items? 10.
#
# The number of ways to insert can be counted via the "bionomial coefficient": bc(m, k) = m!/(k!(m-k)!), where m is the
# total number of items (5 in the example above) and k is the number of selections (2 in the example above). For the
# example above:
#
# bc(5, 2) = 5!/(2!(5-2)!) = 10
#
# Since the SSS can be any arbitrary nucleotide sequence of 3, we count the number of different representations that are
# possible for SSS: 4^3 = 4*4*4 = 64 (4^3, 4 because a nucleotide can be one of ACTG, 3 because the length is 3). In
# each of these representations, the 2-mer AA can be inserted in 10 different ways:
#
# 64*10 = 640
#
# Since the total length of the sequence is 7, we count the number of different representations that are possible:
#
# 4^7 = 4*4*4*4*4*4*4 = 16384
#
# The estimated probability is 640/16384. For non-overlapping k-mers the estimation will actually be "relatively
# accurate", while for overlapping k-mers not so much. Maybe try training a deep learning model to see if it can provide
# better estimates?

# MARKDOWN
def estimate_probability(searchspace_len: int, searchspace_symbol_count: int, search_for: List[int], min_occurrence: int) -> float:
    def factorial(num):
        if num == 1:
            return num
        else:
            return num * factorial(num - 1)

    def bc(m, k):
        return factorial(m) / (factorial(k) * factorial(m - k))

    k = len(search_for)
    n = (searchspace_len - min_occurrence * k)
    return bc(n + min_occurrence, min_occurrence) * (searchspace_symbol_count ** n) / searchspace_symbol_count ** searchspace_len
# MARKDOWN


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        kmer = input()
        seq_len = int(input())

        nuc_to_int = {
            'A': 0,
            'C': 1,
            'T': 2,
            'G': 3
        }
        kmer = kmer.upper()

        print(f'Estimating probability of {kmer} in arbitrary sequence of length {seq_len}\n\n')
        prob  = estimate_probability(seq_len, 4, [nuc_to_int[nuc] for nuc in kmer], 1)
        print(f'Probability: {prob}\n\n')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()