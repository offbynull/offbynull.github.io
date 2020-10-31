import hashlib
import textwrap

import matplotlib.pyplot as plt


# MARKDOWN
def gc_skew(seq: str):
    counter = 0
    skew = [counter]
    for i in range(len(seq)):
        if seq[i] == 'G':
            counter += 1
            skew.append(counter)
        elif seq[i] == 'C':
            counter -= 1
            skew.append(counter)
        else:
            skew.append(counter)
    return skew
# MARKDOWN


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        seq = input()
        print(f'Calculating skew for: {textwrap.shorten(seq, width=15, placeholder="...")}\n')

        skew = gc_skew(seq)

        print(f'Result: {textwrap.shorten(str(skew), width=15, placeholder="...")}\n')

        plot_filename = 'skew_' + hashlib.md5(seq.encode()).hexdigest() + '.png'
        plt.plot(skew)
        plt.ylabel('skew')
        plt.savefig(f'/output/{plot_filename}')

        print(f'![GC Skew Plot]({plot_filename})')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()