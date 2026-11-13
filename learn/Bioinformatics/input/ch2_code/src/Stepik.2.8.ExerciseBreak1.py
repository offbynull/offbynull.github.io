# This is giving back the wrong answer. I'm not sure why. I've spent about 5 hours on this so far.
#
# There are 586 15-mers in a string of 600. The odds of selecting the implanted 15-mer is 1/586. The odds of selecting a
# 15-mer that isn't the implanted one is 585/586.
#
# There are 10 of these 600 length strings, each of which has the implanted 15-mer. Selecting the correct 15-mer in only
# 1 of these 10 strings would have the odds 1/586 * (585/586)^9.
#
# Since we're looking for the odds that there'll be at least 1, we need to go through and include the odds for cases
# where more than 1 of the 10 strings hits the implanted 15-mer...
#
# (1/586)^1 * (585/586)^9 + (1/586)^2 * (585/586)^8 + (1/586)^3 * (585/586)^7 + ... + (1/586)^10 * (585/586)^0
#
# The answer I'm getting is 0.0016833315, which the site is telling me is wrong. What am I missing?


# Erika Lorena Álvarez Ramírez
# Sun, 2 Aug, 22:49 (12 hours ago)
# to me
#
# Hi Kasra. It's fine your probability of missing the implanted k-mer in one string, 1-1/(600-15+1)=585/586.
# After that I don't follow you, because when there is a problem about "at least 1", the easier way to solve it is
# substracting the probability of exactly 0 to the total probability, 1-P(miss all the kmers), and the probability to
# miss all the kmers is P(miss 1 k-mer in one tring)**10, because there are 10 strings,..., now you can solve it!, the
# correct answer is around 10 times your result, good luck!

str_count = 10
str_len = 600
k = 15
min_num_of_correct_selections = 2

num_of_kmers_in_str = str_len - k + 1
odds_of_picking_implanted_kmer_in_str = 1 / num_of_kmers_in_str
odds_of_picking_nonimplanted_kmer_in_str = (num_of_kmers_in_str - 1) / num_of_kmers_in_str

odds = 1.0 - odds_of_picking_nonimplanted_kmer_in_str ** 10

print("{:.10f}". format(odds))
