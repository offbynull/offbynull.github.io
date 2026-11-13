# a random 9-mer in a random seq of len 1000
prob_of_random_9mer = 0.25 ** 9
prob_of_the_same_randomized_9mer_appearing_in_str_of_1000 = prob_of_random_9mer * (1000 - 9 + 1)
prob_of_the_same_randomized_9mer_appearing_in_str_of_1000_for_500_instances = prob_of_the_same_randomized_9mer_appearing_in_str_of_1000 * 500

print(f'{prob_of_the_same_randomized_9mer_appearing_in_str_of_1000_for_500_instances}')