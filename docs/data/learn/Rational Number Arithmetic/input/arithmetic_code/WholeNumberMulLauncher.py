import inspect

from WholeNumber import WholeNumber, log_whitelist

def main():
    log_whitelist([(inspect.getfile(WholeNumber), '__mul__'), (inspect.getfile(WholeNumber), '_single_digit_mul')])

    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        args = input().split()  # read from stdin
        input1 = WholeNumber.from_str(args[0])
        input2 = WholeNumber.from_str(args[1])
        res = input1 * input2  # this will output markdown to stdout
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")

if __name__ == '__main__':
    main()