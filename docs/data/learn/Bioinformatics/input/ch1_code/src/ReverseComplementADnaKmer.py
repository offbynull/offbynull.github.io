from __future__ import annotations


# MARKDOWN
def reverse_complement(strand: str):
    ret = ''
    for i in range(0, len(strand)):
        base = strand[i]
        if base == 'A' or base == 'a':
            base = 'T'
        elif base == 'T' or base == 't':
            base = 'A'
        elif base == 'C' or base == 'c':
            base = 'G'
        elif base == 'G' or base == 'g':
            base = 'C'
        else:
            raise Exception('Unexpected base: ' + base)

        ret += base
    return ret[::-1]
# MARKDOWN


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        seq = input()
        revcomp_seq = reverse_complement(seq)
        print(f'Original: {seq}\n')
        print(f'Reverse Complement: {revcomp_seq}')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()