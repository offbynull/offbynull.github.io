# Let us call [l,r][l,r] the champion interval, if its right endpoint is the smallest among all right endpoints: for any
# other interval [l′,r′][l′,r′], it holds that r≤r′r≤r′. It turns out that the following greedy algorithm maximizes the
# number of non-overlapping segments: take the champion interval, remove all intervals that intersect it, and iterate.
#
# Exercise Break: Prove that if a set of non-overlapping intervals does not contain the champion interval, then
# substituting the first interval in this set by the champion interval results in a set of non-overlapping intervals.


# My answer:
#
# The champion interval has the smallest right endpoint. So everything further must have a larger right endpoint. So
# the first interval in the set may overlap with the champion endpoint, but since it's right point is greater than the
# champion end points right endpoint, removing it and replacing it with the champion endpoint (substituting it) won't
# cause any overlaps in the set
#
# This doesn't really prove anything but I think the thought process is correct here.
