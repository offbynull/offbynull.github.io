import inspect

from FractionNumber import FractionNumber
from Output import log_whitelist

def main():
    log_whitelist([(inspect.getfile(FractionNumber), 'simplify')])

    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        args = input().split()  # read from stdin
        input1 = FractionNumber.from_str(args[0])
        res = input1.simplify()  # this will output markdown to stdout
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")

if __name__ == '__main__':
    main()