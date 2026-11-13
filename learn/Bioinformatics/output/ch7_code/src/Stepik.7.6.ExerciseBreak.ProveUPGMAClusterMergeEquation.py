# EXERCISE BREAK
# --------------
# Exercise Break: Prove that after merging clusters Ci and Cj into a cluster Cnew, ...
#
# dist(Cnew, Cm) =
#    dist(Ci,Cm) * len(Ci) + dist(Cj,Cm) * len(Cj)
#    ---------------------------------------------
#             len(Ci) + len(Cj)


# THE ANSWER BELOW IS WRONG BECAUSE I MESSED UP INTERPRETING THE FORMULA -- THE FORMULAS THAT I STARTED OFF WITH WERE INCORRECT
# THE ANSWER BELOW IS WRONG BECAUSE I MESSED UP INTERPRETING THE FORMULA -- THE FORMULAS THAT I STARTED OFF WITH WERE INCORRECT
# THE ANSWER BELOW IS WRONG BECAUSE I MESSED UP INTERPRETING THE FORMULA -- THE FORMULAS THAT I STARTED OFF WITH WERE INCORRECT
# THE ANSWER BELOW IS WRONG BECAUSE I MESSED UP INTERPRETING THE FORMULA -- THE FORMULAS THAT I STARTED OFF WITH WERE INCORRECT
# THE ANSWER BELOW IS WRONG BECAUSE I MESSED UP INTERPRETING THE FORMULA -- THE FORMULAS THAT I STARTED OFF WITH WERE INCORRECT
# THE ANSWER BELOW IS WRONG BECAUSE I MESSED UP INTERPRETING THE FORMULA -- THE FORMULAS THAT I STARTED OFF WITH WERE INCORRECT
# THE ANSWER BELOW IS WRONG BECAUSE I MESSED UP INTERPRETING THE FORMULA -- THE FORMULAS THAT I STARTED OFF WITH WERE INCORRECT
# THE ANSWER BELOW IS WRONG BECAUSE I MESSED UP INTERPRETING THE FORMULA -- THE FORMULAS THAT I STARTED OFF WITH WERE INCORRECT
# THE ANSWER BELOW IS WRONG BECAUSE I MESSED UP INTERPRETING THE FORMULA -- THE FORMULAS THAT I STARTED OFF WITH WERE INCORRECT
# THE ANSWER BELOW IS WRONG BECAUSE I MESSED UP INTERPRETING THE FORMULA -- THE FORMULAS THAT I STARTED OFF WITH WERE INCORRECT
# THE ANSWER BELOW IS WRONG BECAUSE I MESSED UP INTERPRETING THE FORMULA -- THE FORMULAS THAT I STARTED OFF WITH WERE INCORRECT


# MY ATTEMPT AT ANSWERING
# -----------------------
# Cnew = Ci + Cj  # assumption here is Ci and Cj don't have any of the same nodes
#
# dist(Ci, Cm) =
#      sum(dist_mat[i][j] for i, j in zip(Ci, Cm))
#      -------------------------------------------
#                 len(Ci) * len(Cm)
#
# dist(Cj, Cm) =
#      sum(dist_mat[i][j] for i, j in zip(Cj, Cm))
#      -------------------------------------------
#                 len(Cj) * len(Cm)
#
# dist(Cnew, Cm) =
#      sum(dist_mat[i][j] for i, j in zip(Cnew, Cm))
#      ---------------------------------------------
#                 len(Cnew) * len(Cm)


#    Cnew = Ci | Cj  (EACH CLUSTER'S LEAF NODES ARE UNIQUE TO IT)
#    len(Cnew) = len(Ci) + len(Cj)
#    sum(dist_mat[i][j] for i, j in zip(Cnew, Cm)) = sum(dist_mat[i][j] for i, j in zip(Ci, Cm)) +
#                                                    sum(dist_mat[i][j] for i, j in zip(Cj, Cm))
#
# Is the last one correct?
#
#      sum(dist_mat[i][j] for i, j in zip(Ci, Cm)) + sum(dist_mat[i][j] for i, j in zip(Cj, Cm))
#      -----------------------------------------------------------------------------------------
#                                   len(Ci) + len(Cj) + len(Cm)


# Maybe this requires some substitution, algebra, and finessing to get the BELOW dist(Cnew, Cm) to look like the ABOVE
# dist(Cnew, Cm)?
#
# I'm struggling to sort this one out at the moment.
