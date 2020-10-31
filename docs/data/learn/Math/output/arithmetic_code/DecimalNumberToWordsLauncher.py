import inspect

from DecimalNumber import DecimalNumber
from FractionNumber import FractionNumber
from IntegerNumber import IntegerNumber
from WholeNumber import WholeNumber, log_whitelist

def main():
    log_whitelist([(inspect.getfile(DecimalNumber), 'to_words')])

    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        args = input().split()  # read from stdin
        input1 = DecimalNumber.from_str(args[0])
        res = input1.to_words()  # this will output markdown to stdout
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")

if __name__ == '__main__':
    main()