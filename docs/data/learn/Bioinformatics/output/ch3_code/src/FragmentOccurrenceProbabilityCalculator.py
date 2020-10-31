from collections import Counter
from random import Random
from typing import Dict, List, TypeVar, Optional, Tuple

from Graph import Graph
from Read import Read
from ReadPair import ReadPair
from ToDeBruijnGraph import to_debruijn_graph
from Utils import generate_random_genome, count_kmers

T = TypeVar('T', Read, ReadPair)


# MARKDOWN
# If less than 50% of the reads are from repeats, this attempts to count and normalize such that it can hint at which
# reads may contain errors (= ~0) and which reads are for repeat regions (> 1.0).
def calculate_fragment_occurrence_probabilities(fragments: List[T]) -> Dict[T, float]:
    counter = Counter(fragments)
    max_digit_count = max([len(str(count)) for count in counter.values()])
    for i in range(max_digit_count):
        rounded_counter = Counter(dict([(k, round(count, -i)) for k, count in counter.items()]))
        for k, orig_count in counter.items():
            if rounded_counter[k] == 0:
                rounded_counter[k] = orig_count
        most_occurring_count, times_counted = Counter(rounded_counter.values()).most_common(1)[0]
        if times_counted >= len(rounded_counter) * 0.5:
            return dict([(key, value / most_occurring_count) for key, value in rounded_counter.items()])
    raise ValueError(f'Failed to find a common count: {counter}')
# MARKDOWN


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        lines = []
        while True:
            try:
                line = input().strip()
                if len(line) > 0:
                    lines.append(line)
            except EOFError:
                break

        frag_to_count = [l.split() for l in lines]
        print(f'Sequenced fragments:', end='\n\n')
        for f in frag_to_count:
            print(f' * {f[0]} was scanned in {f[1]} times.')
        raw_reads = [read for e in frag_to_count for read in [Read(e[0])] * int(e[1])]
        occurrence_probabilities = calculate_fragment_occurrence_probabilities(raw_reads)
        print(f'', end='\n\n')
        print(f'Probability of occurrence in genome:', end='\n\n')
        for read, appearances in occurrence_probabilities.items():
            print(f' * {read} probably has {appearances} appearances in the genome.')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()
# if __name__ == '__main__':
#     r = Random(126)
#
#     genome_len = 50
#     k_read = 12
#     k_break = 6
#
#     genome = generate_random_genome(genome_len, r=r)
#     reads = Read.random_fragment(genome, k_read, count_kmers(genome_len, k_read) * 30, r=r)
#     reads[0] = reads[0].introduce_random_errors(1, r=r)
#     reads = [broken_read for read in reads for broken_read in read.shatter(k_break)]
#     normalized_read_counts = normalize_based_on_occurrence_counts(reads)
#     print(f'{normalized_read_counts}')
#     reads = reads[0].collapse(reads)
#     graph = to_debruijn_graph(reads)
#     print(to_graphviz(graph, normalized_read_counts))
#     potentially_bad_paths = find_bubbles(graph, k_break)\
#                             + find_head_convergences(graph, k_break)\
#                             + find_tail_divergences(graph, k_break)
#     for src, branch, dst in potentially_bad_paths:
#         print(f'Src: {src}, Dst: {dst}, Branch: {"->".join([str(x) for x in branch])}')
