import lzma

from FindMaximalNonBranchingPaths import find_maximal_non_branching_paths
from Kdmer import Kdmer
from Read import Read
from ReadPair import ReadPair
from ToDeBruijnGraph import to_debruijn_graph

reads_filepath = 'FinalChallengeReads.txt.xz'
with lzma.open(reads_filepath, mode='rt', encoding='utf-8') as f:
    lines = f.read().splitlines()
    lines = [l.strip() for l in lines]  # get rid of whitespace
    lines = [l for l in lines if len(l) > 0]  # get rid of empty lines

lines_split = [tuple(l.split('|', maxsplit=2)) for l in lines]
kdmers = [Kdmer(k1, k2, 1000) for k1, k2 in lines_split]
rps = [ReadPair(kdmer) for kdmer in kdmers]
broken_rps = [broken_rp for rp in rps for broken_rp in rp.shatter(40)]

broken_rps = list(set(broken_rps))

graph = to_debruijn_graph(broken_rps)
contig_paths = find_maximal_non_branching_paths(graph)

contig_paths.sort(key=lambda x: len(x))

for path in contig_paths:
    if len(path) >= path[0].d:
        out = path[0].stitch(path)
        print(f'{len(path)} kd-mers = {out}')
    else:
        heads = [Read(p.data.head) for p in path]
        heads_out = heads[0].stitch(heads)
        tails = [Read(p.data.tail) for p in path]
        tails_out = tails[0].stitch(tails)
        print(f'{len(heads)} k-mers = {heads_out}')
        print(f'{len(tails)} k-mers = {tails_out}')
