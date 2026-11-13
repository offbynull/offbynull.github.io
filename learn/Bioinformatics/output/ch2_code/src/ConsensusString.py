from collections import Counter
from typing import Dict, List

# MARKDOWN
def get_consensus_string(kmers: List[str]) -> str:
    count = len(kmers[0]);
    out = ''
    for i in range(0, count):
        c = Counter()
        for kmer in kmers:
            c[kmer[i]] += 1
        ch = c.most_common(1)
        out += ch[0][0]
    return out
# MARKDOWN


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        kmers = []
        while True:
            try:
                kmer = input().strip()
                if len(kmer) > 0:
                    kmers.append(kmer)
            except EOFError:
                break

        consensus_str = get_consensus_string(kmers)
        print(f'Consensus is {consensus_str} in <br><br> {"<br>".join(kmers)}')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()