# Exercise Break: Exercise Break: The figure below illustrates two ways of clustering the data from the figure on the
# previous step. Find the remaining eight ways of clustering these data using the same tree.
#
#      ORIGINAL
#             .-g3
#           .-*
#  .--------* '-g5
#  |        '---g8
# -*   .--------g7
#  | .-* .------g1
#  | | '-*
#  '-*   '------g6
#    |   .------g10
#    | .-* .----g2
#    '-* '-*
#      |   '----g4
#      '--------g9
#
#
#
#   CUT HERE                         CUT HERE
#       v                               v
#       |     .-g3                      |     .-g3
#       |   .-*                         |   .-*
#  .----|---* '-g5                 .----|---* '-g5
#  |    |   '---g8                 |    |   '---g8
# -*   .|-------g7                -*   .|-------g7
#  | .-*|.------g1                 | .-*|.------g1
#  | | '|*                         | | '|*
#  '-*  |'------g6                 '-*  |'------g6
#    |  |.------g1                   |  |.------g1
#    | .|* .----g2                   | .|* .----g2
#    '-*|'-*                         '-*|'-*
#      ||  '----g4                     ||  '----g4
#      '|-------g9                     '|-------g9


# MY ANSWER
# ---------
# If you move the cut line before each of the remaining merge points to reveal the different clusterings in the tree.
# For example...
#
#           CUT HERE                       CUT HERE                          CUT HERE
#              v                              v                                 v
#             .|g3                            |.-g3                             |  .-g3
#           .-*|                             .|*                                |.-*
#  .--------* '|g5                  .--------*|'-g5                     .-------|* '-g5
#  |        '--|g8                  |        '|--g8                     |       |'---g8
# -*   .-------|g7                 -*   .-----|--g7                    -*   .---|----g7
#  | .-* .-----|g1                  | .-* .---|--g1                     | .-* .-|----g1
#  | | '-*     |                    | | '-*   |                         | | '-* |
#  '-*   '-----|g6                  '-*   '---|--g6                     '-*   '-|----g6
#    |   .-----|g10                   |   .---|--g10                      |   .-|----g10
#    | .-* .---|g2                    | .-* .-|--g2                       | .-* |----g2
#    '-* '-*   |                      '-* '-* |                           '-* '-|
#      |   '---|g4                      |   '-|--g4                         |   |----g4
#      '-------|g9                      '-----|--g9                         '---|----g9








