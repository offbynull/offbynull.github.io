import inspect

from DecimalNumber import DecimalNumber
from FractionNumber import FractionNumber
from IntegerNumber import IntegerNumber
from WholeNumber import WholeNumber, log_whitelist

def main():
    log_whitelist([(inspect.getfile(DecimalNumber), 'round')])

    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        args = input().split(None, 2)  # read from stdin
        input1 = DecimalNumber.from_str(args[0])
        input2 = args[1].strip()
        res = input1.round(input2)  # this will output markdown to stdout
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")

if __name__ == '__main__':
    main()