from typing import List

from BruteforceProbabilityOfKmerInArbitrarySequence import bruteforce_probability

found, found_max = bruteforce_probability(25, 2, [0, 1], 1)
print(f'{found}/{found_max}')

#  This takes ~7 mins to run, which is not great. There's another solution in the comments that makes use of probability
#  reasoning to come up with a faster computation. I didn't understand how it worked.
