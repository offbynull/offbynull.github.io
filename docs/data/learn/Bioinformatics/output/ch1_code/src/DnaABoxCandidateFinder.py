import hashlib
import textwrap
import lzma
import matplotlib.pyplot as plt


# MARKDOWN
from FindLocations import Options
from FindRepeatingInWindow import scan_for_repeating_kmers_in_clusters


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
        filepath = input()
        with lzma.open(filepath, mode='rt', encoding='utf-8') as f:
            lines = f.read().splitlines()
            lines = [line for line in lines if not line.startswith('>')]
            seq = ''.join(lines)

        print(f'Calculating skew for: {textwrap.shorten(seq, width=15, placeholder="...")}\n')

        skew = gc_skew(seq)

        print(f'Result: {textwrap.shorten(str(skew), width=15, placeholder="...")}\n')

        plot_filename = 'skew_' + hashlib.md5(seq.encode()).hexdigest() + '.png'
        plt.plot(skew)
        plt.ylabel(f'{filepath} skew')
        plt.savefig(f'/output/{plot_filename}')

        ori_vicinity = skew.index(min(skew))
        print(f'![GC Skew Plot]({plot_filename})\n')
        print(f'Ori vicinity (min pos): {ori_vicinity}\n')

        k = 9
        min_occurrence_in_cluster = 3
        cluster_window_size = 500
        hamming_distance = 1
        reverse_comp = True

        ori_vicinity_seq = seq[ori_vicinity - 500:ori_vicinity + 500]
        scan_res = scan_for_repeating_kmers_in_clusters(ori_vicinity_seq,
                                                        k,
                                                        min_occurrence_in_cluster,
                                                        cluster_window_size,
                                                        Options(hamming_distance, reverse_comp))
        scan_res = list(scan_res)
        scan_res = sorted(scan_res, key=lambda found: (found.start_index, found.occurrence_count))
        print(f'In the ori vicinity, found clusters of k={k} (at least {min_occurrence_in_cluster} occurrences in window of {cluster_window_size}) in {textwrap.shorten(ori_vicinity_seq, width=15, placeholder="...")} at...')
        [print(f' * {found}') for found in scan_res]
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()