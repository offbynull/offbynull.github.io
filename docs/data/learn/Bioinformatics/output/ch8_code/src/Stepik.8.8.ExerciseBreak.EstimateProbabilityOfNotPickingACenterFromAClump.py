# Exercise Break: Estimate the probability that at least one of the five clumps in the figure below will have no centers
# if five centers are chosen randomly from the data (like in the Lloyd algorithm).  Note: to estimate the probability,
# assume that we can choose the same center more than once; that is, we can choose centers "with replacement".

# The picture below is a bunch of dots, each in a clump. There are 5 clumps in total, and each clump has 10 points.

# MY ANSWER
# ---------
# PROBABILITY THAT 5 POINTS ARE CHOSEN, 1 IN EACH CLUMP...
#  - In the first round of selection, any point you pick will be in 1 of the 5 clumps (100% chance of selecting within a
#    clump): 50/50
#  - In the second round of selection, the 10 points making up the clump that the last chosen point is form is off
#    limits: 40/50
#  - In the third round of selection, the 20 points making up the clumps that the last 2 chosen points are from form are
#    off limits: 30/50
#  - ...
# Probability of choosing 5 points where 1 point ends up in each clump: 50/50 * 40/50 * 30/50 * 20/50 * 10/50 = 0.0384
#
# WE WANT THE OPPOSITE OF THE ABOVE: At least one of the clumps has no centers chosen...
#
# 1-(50/50 * 40/50 * 30/50 * 20/50 * 10/50) = 0.9616

# SEE https://iitutor.com/probability-with-replacement/
