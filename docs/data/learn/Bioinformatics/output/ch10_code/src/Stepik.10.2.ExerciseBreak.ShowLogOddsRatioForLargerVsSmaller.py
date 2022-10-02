# Exercise Break: Show that Pr(x|F) is larger than Pr(x|B) when the log-odds ratio is positive
# (i.e., when k/n < 1/ log2(3)) and smaller than Pr(x|B) when the log-odds ratio is negative
# (i.e., when k/n > 1/ log2(3)).


# My answer:
#
# When Pr(x|F) > Pr(x|B), Pr(x|F) / Pr(x|B) will be > 1.0. As such, log2 of that will be > 0
# When Pr(x|F) < Pr(x|B), Pr(x|F) / Pr(x|B) will be < 1.0. As such, log2 of that will be < 0
#
#    | Pr(x|F)/Pr(x|B) | log2(Pr(x|F)/Pr(x|B)) |
#    |-----------------|-----------------------|
#    | 0.015625 (1/64) | -6                    |
#    | 0.03125  (1/32) | -5                    |
#    | 0.0625   (1/16) | -4                    |
#    | 0.125    (1/8)  | -3                    |
#    | 0.25     (1/4)  | -2                    |
#    | 0.5      (1/2)  | -1                    |
#    | 1               | 0                     |
#    | 2               | 1                     |
#    | 4               | 2                     |
#    | 8               | 3                     |
#    | 16              | 4                     |
#    | 32              | 5                     |
#    | 64              | 6                     |
#
