# Exercise Break: Given the PAM250 scoring matrix, an amino acid k-mer Peptide, and a threshold θ, develop an efficient
# algorithm for finding the exact number of k-mers scoring more than θ against Peptide.
#
# MY ANSWER
# ---------
# This might have to do with pruning. The scoring matrix has a min and a max value: -8 to 18. There are k symbols we
# need, and we have to reach a threshold of theta.
#
# Start with a root node and branch of all possible symbol. For each edge, assign the min value for that symbol in the
# PAM matrix.
#
# Now there are k-1 nodes. For each branch, we recurse into it only continue if (k-1) * 18 > threshold -- 18 is the max
# possible value

pam250_data = """
   A  C  D  E  F  G  H  I  K  L  M  N  P  Q  R  S  T  V  W  Y
A  2 -2  0  0 -3  1 -1 -1 -1 -2 -1  0  1  0 -2  1  1  0 -6 -3
C -2 12 -5 -5 -4 -3 -3 -2 -5 -6 -5 -4 -3 -5 -4  0 -2 -2 -8  0
D  0 -5  4  3 -6  1  1 -2  0 -4 -3  2 -1  2 -1  0  0 -2 -7 -4
E  0 -5  3  4 -5  0  1 -2  0 -3 -2  1 -1  2 -1  0  0 -2 -7 -4
F -3 -4 -6 -5  9 -5 -2  1 -5  2  0 -3 -5 -5 -4 -3 -3 -1  0  7
G  1 -3  1  0 -5  5 -2 -3 -2 -4 -3  0  0 -1 -3  1  0 -1 -7 -5
H -1 -3  1  1 -2 -2  6 -2  0 -2 -2  2  0  3  2 -1 -1 -2 -3  0
I -1 -2 -2 -2  1 -3 -2  5 -2  2  2 -2 -2 -2 -2 -1  0  4 -5 -1
K -1 -5  0  0 -5 -2  0 -2  5 -3  0  1 -1  1  3  0  0 -2 -3 -4
L -2 -6 -4 -3  2 -4 -2  2 -3  6  4 -3 -3 -2 -3 -3 -2  2 -2 -1
M -1 -5 -3 -2  0 -3 -2  2  0  4  6 -2 -2 -1  0 -2 -1  2 -4 -2
N  0 -4  2  1 -3  0  2 -2  1 -3 -2  2  0  1  0  1  0 -2 -4 -2
P  1 -3 -1 -1 -5  0  0 -2 -1 -3 -2  0  6  0  0  1  0 -1 -6 -5
Q  0 -5  2  2 -5 -1  3 -2  1 -2 -1  1  0  4  1 -1 -1 -2 -5 -4
R -2 -4 -1 -1 -4 -3  2 -2  3 -3  0  0  0  1  6  0 -1 -2  2 -4
S  1  0  0  0 -3  1 -1 -1  0 -3 -2  1  1 -1  0  2  1 -1 -2 -3
T  1 -2  0  0 -3  0 -1  0  0 -2 -1  0  0 -1 -1  1  3  0 -5 -3
V  0 -2 -2 -2 -1 -1 -2  4 -2  2  2 -2 -1 -2 -2 -1  0  4 -6 -2
W -6 -8 -7 -7  0 -7 -3 -5 -3 -2 -4 -4 -6 -5  2 -2 -5 -6 17  0
Y -3  0 -4 -4  7 -5  0 -1 -4 -1 -2 -2 -5 -4 -4 -3 -3 -2  0 10
""".strip()
rows = pam250_data.split('\n')
header = rows[0].split()
rows = [r.split() for r in rows[1:]]
pam250 = {}
for i, r in enumerate(rows):
    colA = r[0]
    for j, val in enumerate(r[1:]):
        colB = header[j]
        pam250[colA, colB] = int(val)

min_value = min(pam250.values())
max_value = max(pam250.values())

def recurse(kmer: str, prefix: str, score: int, threshold_score: int):
    if kmer == '':
        return 1
    remaining = len(kmer)
    if remaining * max_value < threshold_score:
        return 0
    found = 1
    for symbol in header:
        elem_score = pam250[symbol, kmer[-1]]
        found += recurse(kmer[1:], prefix + symbol, score + elem_score, threshold_score)
    return found

count = recurse('ACID', '', 0, 10)
print(f'{count}')


# THIS SEEMS LIKE IT WORKS. This qualifies as a "branch-and-bound" algorithm.
#
# One modification could be to cache scores for a contiguous subsequence so that you can do more than 1 symbol at a
# time. Is this "dynamic programming"?, if is there a better "dynamic programming" way of doing this?
