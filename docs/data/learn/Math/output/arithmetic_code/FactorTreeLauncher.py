import inspect

import Factor
from Factor import factor_naive, is_prime, factor_tree
from WholeNumber import WholeNumber
from Output import log_whitelist

def main():
    log_whitelist([(inspect.getfile(Factor), 'factor_tree')])

    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        args = input().split()  # read from stdin
        input1 = WholeNumber.from_str(args[0])
        res = factor_tree(input1)  # this will output markdown to stdout
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")

if __name__ == '__main__':
    main()