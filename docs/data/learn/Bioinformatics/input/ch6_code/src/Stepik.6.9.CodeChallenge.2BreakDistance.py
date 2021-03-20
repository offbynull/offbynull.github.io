from typing import List, Tuple

from GenomeGraph import GenomeGraph

with open('/home/user/Downloads/dataset_240324_4.txt', mode='r', encoding='utf-8') as f:
    data = f.read()

lines = data.split('\n')
p_list1 = [[int(x) for x in s.split(' ')] for s in lines[0][1:-1].split(')(')]
p_list2 = [[int(x) for x in s.split(' ')] for s in lines[1][1:-1].split(')(')]


def walk_cycle(gg: GenomeGraph, start_nid: Tuple[int, str]):
    next_nid = start_nid
    eids = []
    eids_quick_lookup = set()
    while next_nid is not None:
        curr_nid = next_nid
        next_nid = None
        for eid in gg.get_edges(curr_nid):
            if eid in eids_quick_lookup:  # don't explore if it's already been walked
                continue
            eids.append(eid)
            eids_quick_lookup.add(eid)
            nid1, nid2 = gg.get_edge_endpoints(eid)
            if nid1 == curr_nid:
                next_nid = nid2
            else:
                next_nid = nid1
    return eids


gg = GenomeGraph()
for i, p in enumerate(p_list1):
    gg.add_permutation(p)
for i, p in enumerate(p_list2):
    gg.add_permutation(p)

cycles = []
nid_queue = {nid for nid in gg.all_nodes()}
while nid_queue:
    nid = next(iter(nid_queue))
    cycle = walk_cycle(gg, nid)
    cycles.append(cycle)
    [nid_queue.discard(n) for e in cycle for n in gg.get_edge_endpoints(e)]

block_count = sum(1 for x in gg.all_nodes()) // 2
cycle_count = len(cycles)

print(f'{block_count - cycle_count}')