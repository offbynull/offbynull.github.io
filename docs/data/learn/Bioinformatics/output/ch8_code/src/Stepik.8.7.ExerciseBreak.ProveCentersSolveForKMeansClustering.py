# Exercise Break: Prove that the centers below solve the k-Means Clustering Problem for the black data points shown when
# k = 3.
#
#
# (5/3, 13/3)
#       (1, 3)
#       (1, 5)
#       (3, 6)
# (6.5, 6.5)
#       (6, 5)
#       (8, 7)
# (22/3, 2)
#       (5, 2)
#       (7, 1)
#       (10, 3)


# MY ANSWER
# ---------
# I'm not sure how to prove this exactly, but the 2nd center point (6.5, 6.5) obviously solves for that cluster because
# the optimal center point for any cluster with 2 members is exactly half way between the line that the 2 points make. I
# "proved" this in the "Prove Farthest First Traversal Sub Optimal Constraint" exercise break back in section 8.6.
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
#
#   def squared_error_distortion(data_pts, center_pts):
#       res = []
#       for data_pt in data_pts:
#           closest_center_pt, dist_to = find_closest_center(data_pt, center_pts)
#           res.append(dist_to ** 2)
#       return sum(res) / len(res)
#
# It turns out that (6.5, 6.5) is exactly between the line between points (6, 5) and (8, 7), so I'm not sure what else
# there is to "prove"? If you shift the center point towards either of the members, the squared error distortion would
# grow...
#   (6.5^2 + 6.5^2) ÷ 2 = 42.25
#   (6^2 + 7^2) ÷ 2 = 42.5
#   (7^2 + 6^2) ÷ 2 = 42.5
#
# Why is this the case? As soon as the center point skews more so towards a member, one of the distances will be larger.
# A larger base with the same exponent expands faster vs smaller base...
#   2^2 = 4
#   3^2 = 9
#   4^2 = 16
#   5^2 = 25
#
# By making the base in one of the operands larger and the base in the other operand smaller (by the same difference),
# you're pretty much guaranteeing a larger squared_error_distortion. The larger base adds more than the smaller base
# takes away.
#
# FOR THE OTHERS, I'm not sure. The only way the squared error distortion sinks lower is if the center inches closer to
# one of the 3 member points. As soon as the distance to one member shrinks, the distance to the other members will
# grow, and the same exponent dynamic detailed for the 2 member (6.5, 6.5) cluster will apply for the 3 member
# clusters. The loss from the shortening of a distance to one of the members needs to be lower than the gain from
# lengthening the distances to the other members.
#
# (5/3, 13/3)
#       (1, 3)
#       (1, 5)
#       (3, 6)
#
# How exactly does this prove anything? You can sit here and try knocking the center point towards each point by ultra
# small amounts to see if it clowers the squared error distortion, but that doesn't seem like a robuse "proof". I don't
# know.
#
# How about this. In the 3 point clusters, it almost looks as if the center point started off as sitting halfway in
# between one of the lines (any) made up by 2 of the 3 members, and then when the 3rd member was added the center point
# got dragged in a straight-line towards it.
#
# So maybe the "proof here" is a divide-and-conquer algorithm. For example, start off with the center point exactly
# half way between (A,B).
#
#           C
#
#
#
#
#      A    *    B
#           ^
#           '---- center between A and B
#
# Move the center point exactly half-way towards C in a straight-line.
#
#            C
#
#
#            *   <--- center moved up halfway towards C
#
#       A         B
#
# Then, test the error squared distortion in the case where it cuts half way up vs half way down.
#
#             C                                            C
#
#             *   <-- center moved up halfway
#
#                                                          * <-- center moved down halfway
#        A         B                                  A         B
#
# Choose the side that produced the lower squared error distortion and repeat, limiting to that side. Eventually you'll
# converge on the exact solution (or near exact solution if it isn't divisible by 2).
#
# But, I don't think this is the type of proof they're looking for. It wants a "math"-ish proof. I don't know where to
# start with that. I've already tried listing out the squared_error_distortion equation and tried to manipulate it but
# ended up going nowhere.

