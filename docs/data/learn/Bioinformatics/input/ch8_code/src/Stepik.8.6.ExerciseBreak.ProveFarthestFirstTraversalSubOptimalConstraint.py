from statistics import mean

from helpers.GeometryUtils import distance

# Exercise Break: Let Centers be the set of centers returned by FarthestFirstTraversal, and let Centers_opt be a set of
# centers corresponding to an optimal solution of the k-Center Clustering Problem. Prove that
#
# MaxDistance(Data,Centers) ≤ 2 * MaxDistance(Data,Centers_opt).
#
# Can you find a collection of data points such that the centers returned by FarthestFirstTraversal are suboptimal?


# HINT: See Stepik.8.5.CodeChallenge.ComputeMaxDistance if you forgot what MaxDistance does. It first goes over each
# data point and returns the distance to the closest center. Then, it picks the longest distance out of all of those
# closest distances.


# MY ANSWER -- IT IS WRONG (but it might be close)
# ------------------------
# The second part of the question is easy. If you have 4 points {A, B, C, D} as follows ...
#
#
#  │
#  │    A                                 D
#  │
#  │    B                                 C
#  │
#  └─────────────────────────────────────────
#
# and you wanted the 2 most optimal center points, those center points would be ...
#
# 1. a center point in between A and B
# 2. a center point in between C and D
#
# FarthestFirstTraversal wouldn't give you those 2 center points, it would instead select 2 points out of
# {A, B, C, D}.
#
# And I suppose this was a hint that leads to an answer for the proof (the first part of the question). A center point
# returned by FarthestFirstTraversal is only ever going to be an optimal center point in certain cases. For example, the
# 2 center points returned by FarthestFirstTraversal for the following...
#
#  │
#  │    A                                 D
#  │
#  │                                      C
#  │
#  └─────────────────────────────────────────
#
# 1. a center point that is __either__ C or D -- this is sub-optimal because the center point should be __between__ C
#    and D.
# 2. a center point at A -- this is optimal.
#
# For the above, ...
#   MaxDistance(Data,Centers_FarthestFirstTraversal) = dist(C, D)
#   MaxDistance(Data,Centers_opt)                    = dist(C, D) / 2
#
# So sure enough, the condition given in the question holds ...
#   MaxDistance(Data,Centers_FarthestFirstTraversal) ≤ 2 * MaxDistance(Data,Centers_opt)
#   dist(C,D)                                        ≤ 2 * (dist(C,D) / 2)
#   dist(C,D)                                        ≤ dist(C,D)
#
# How does this generalize? Recall exactly what it is that MaxDistance does. It first goes over each data point and
# returns the distance to the closest center. Then, it picks the longest distance out of all of those closest distances.
# When FarthestFirstTraversal, these closest distances are a subset of the data points themselves.
#
# Imagine if a center point were optimal. If there were 2 data points that had it as its closest center (as in the C D
# example above), that center point will be directly in between the data points. The distance between the center point
# and each of the 2 nodes would be exactly the same -- exactly half the distance between C and D.
#
# dist(C,*) = dist(C, D) / 2
# dist(D,*) = dist(E, C) / 2
#
#  │
#  │                  D
#  │
#  │                  *
#  │
#  │                  C
#  │
#  └─────────────────────────────────────────
#
# The moment there are 3 data points that the optimal center is for, that center point will get dragged into another
# direction. That dragging makes it so that the center won't be halfway in between ANY of the pair of data points. That
# is, the distance between the optimal center and any data point will be MORE than the distance between any pair of
# data points / 2 (triangle property, assuming that multiple data points can't occupy the same coordinates).
#
# dist(C,*) > dist(C,D) / 2
# dist(C,*) > dist(C,E) / 2
# dist(D,*) > dist(D,C) / 2
# dist(D,*) > dist(D,E) / 2
# dist(E,*) > dist(E,C) / 2
# dist(E,*) > dist(E,D) / 2
#
#  │
#  │                  D
#  │
#  │                     *    E
#  │
#  │                  C
#  │
#  └─────────────────────────────────────────
#
# The moment there are 4 data points that the optimal center is for, that center point could POSSIBLY get dragged back
# such that it sits directly in between SOME data points.
#
# dist(F,*) = dist(F,E) / 2
# dist(F,*) > dist(F,C) / 2   (because of the triangle property)
#
#  │
#  │                  D
#  │
#  │          F       *       E
#  │
#  │                  C
#  │
#  └─────────────────────────────────────────
#
# Same with 5, 6, 7, 8, ... data points.
#
#
#
# So does this prove it then? The above shows comparisons between distances to other data points vs distances to the
# optimal center. When FarthestFirstTraversal returns centers, those centers ARE other data points (the centers are a
# subset of data points). The condition ...
#
#   MaxDistance(Data,Data_subset) ≤ 2 * MaxDistance(Data,Centers_opt)
#
# ... can be rewritten as ...
#
#   2 * MaxDistance(Data,Centers_opt) ≥ MaxDistance(Data,Data_subset)
#
# ... and then ...
#
#   MaxDistance(Data,Centers_opt) ≥ MaxDistance(Data,Data_Subset) / 2
#
# This is WRONG as the division is happening OUTSIDE the MaxDistance. I think I'm close but this is wrong.
