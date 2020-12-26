# The DAG representing the possible sequence alignments is below. The symbol * represents a node, while → ↓ ↘ represent
# directed edges.
#
#     A   T   C   G   T   C   C
#   * → * → * → * → * → * → * → *
# A ↓ ↘ ↓ ↘ ↓ ↘ ↓ ↘ ↓ ↘ ↓ ↘ ↓ ↘ ↓
#   * → * → * → * → * → * → * → *
# T ↓ ↘ ↓ ↘ ↓ ↘ ↓ ↘ ↓ ↘ ↓ ↘ ↓ ↘ ↓
#   * → * → * → * → * → * → * → *
# G ↓ ↘ ↓ ↘ ↓ ↘ ↓ ↘ ↓ ↘ ↓ ↘ ↓ ↘ ↓
#   * → * → * → * → * → * → * → *
# T ↓ ↘ ↓ ↘ ↓ ↘ ↓ ↘ ↓ ↘ ↓ ↘ ↓ ↘ ↓
#   * → * → * → * → * → * → * → *
# T ↓ ↘ ↓ ↘ ↓ ↘ ↓ ↘ ↓ ↘ ↓ ↘ ↓ ↘ ↓
#   * → * → * → * → * → * → * → *
# A ↓ ↘ ↓ ↘ ↓ ↘ ↓ ↘ ↓ ↘ ↓ ↘ ↓ ↘ ↓
#   * → * → * → * → * → * → * → *
# T ↓ ↘ ↓ ↘ ↓ ↘ ↓ ↘ ↓ ↘ ↓ ↘ ↓ ↘ ↓
#   * → * → * → * → * → * → * → *
# A ↓ ↘ ↓ ↘ ↓ ↘ ↓ ↘ ↓ ↘ ↓ ↘ ↓ ↘ ↓
#   * → * → * → * → * → * → * → *
#
# The DAG below is the same as the one above, but with a path highlighted. The symbols | / \ - are used to highlight the
# path (starts from top-left and finishes at bottom right).
#
#     A   T   C   G   T   C   C
#   * → * → * → * → * → * → * → *
# A | ↘ ↓ ↘ ↓ ↘ ↓ ↘ ↓ ↘ ↓ ↘ ↓ ↘ ↓
#   * → * → * → * → * → * → * → *
# T | ↘ ↓ ↘ ↓ ↘ ↓ ↘ ↓ ↘ ↓ ↘ ↓ ↘ ↓
#   * → * → * → * → * → * → * → *
# G ↓ \ ↓ ↘ ↓ ↘ ↓ ↘ ↓ ↘ ↓ ↘ ↓ ↘ ↓
#   * → * → * → * → * → * → * → *
# T ↓ ↘ ↓ \ ↓ ↘ ↓ ↘ ↓ ↘ ↓ ↘ ↓ ↘ ↓
#   * → * → * → * → * → * → * → *
# T ↓ ↘ ↓ ↘ | ↘ ↓ ↘ ↓ ↘ ↓ ↘ ↓ ↘ ↓
#   * → * → * → * → * → * → * → *
# A ↓ ↘ ↓ ↘ ↓ \ ↓ ↘ ↓ ↘ ↓ ↘ ↓ ↘ ↓
#   * → * → * → * - * → * → * → *
# T ↓ ↘ ↓ ↘ ↓ ↘ ↓ ↘ ↓ \ ↓ ↘ ↓ ↘ ↓
#   * → * → * → * → * → * - * - *
# A ↓ ↘ ↓ ↘ ↓ ↘ ↓ ↘ ↓ ↘ ↓ ↘ ↓ ↘ |
#   * → * → * → * → * → * → * → *
#
# This is an alignment path. Each step ...
#  * down (|) represents keep the left element but discard the top   (INSERT LEFT / DELETE TOP)
#  * right (-) represents keep the top element but discard the left  (DELETE LEFT / INSERT TOP)
#  * diagonal (\) represents keep both elements                      (INSERT LEFT / INSERT TOP)
#
# Given the alignment path above, its text representation would be as follows. Note that the first line represents the
# left sequence while the second line represents the top sequence.
#
# ATGTTA-T--A    (seq from left side of DAG)
# --AT-CGTCC-    (seq from top side of DAG)
#
# There is no code for this. You just look at the DAG and follow the path.
