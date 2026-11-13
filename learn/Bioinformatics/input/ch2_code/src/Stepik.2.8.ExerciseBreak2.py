# See comments in exercise break 1
# See https://math.stackexchange.com/questions/1017787/what-is-the-probability-of-two-out-of-three-events-happening

str_count = 10
str_len = 600
k = 15
min_num_of_correct_selections = 2

num_of_kmers_in_str = str_len - k + 1
odds_of_picking_implanted_kmer_in_str = 1 / num_of_kmers_in_str
odds_of_picking_nonimplanted_kmer_in_str = (num_of_kmers_in_str - 1) / num_of_kmers_in_str

odds_none_found = odds_of_picking_nonimplanted_kmer_in_str ** 10
odds_one_found = (odds_of_picking_implanted_kmer_in_str * odds_of_picking_nonimplanted_kmer_in_str ** 9) * 10
odds = 1.0 - odds_none_found - odds_one_found


print("{:.10f}". format(odds))
