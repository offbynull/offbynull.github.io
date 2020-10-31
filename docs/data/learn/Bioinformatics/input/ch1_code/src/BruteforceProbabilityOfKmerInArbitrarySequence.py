from typing import List


# This implementation tries every possible combination of sequence to find the probability. It falls over once the
# length of the sequence extends into the double digits -- it's a toy implementation to help conceptualize what's
# going on.

# MARKDOWN
# Of the X sequence combinations tried, Y had the k-mer. The probability is Y/X.
def bruteforce_probability(searchspace_len: int, searchspace_symbol_count: int, search_for: List[int], min_occurrence: int) -> (int, int):
    found = 0
    found_max = searchspace_symbol_count ** searchspace_len

    str_to_search = [0] * searchspace_len

    def count_instances():
        ret = 0
        for i in range(0, searchspace_len - len(search_for) + 1):
            if str_to_search[i:i + len(search_for)] == search_for:
                ret += 1
        return ret

    def walk(idx: int):
        nonlocal found

        if idx == searchspace_len:
            count = count_instances()
            if count >= min_occurrence:
                found += 1
        else:
            for i in range(0, searchspace_symbol_count):
                walk(idx + 1)
                str_to_search[idx] += 1
            str_to_search[idx] = 0

    walk(0)

    return found, found_max
# MARKDOWN


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        kmer = input()
        seq_len = int(input())

        nuc_to_int = {
            'A': 0,
            'C': 1,
            'T': 2,
            'G': 3
        }
        kmer = kmer.upper()

        print(f'Brute-forcing probability of {kmer} in arbitrary sequence of length {seq_len}\n\n')
        found, found_max  = bruteforce_probability(seq_len, 4, [nuc_to_int[nuc] for nuc in kmer], 1)
        print(f'Probability: {found/found_max} ({found}/{found_max})\n\n')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()