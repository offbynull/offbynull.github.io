`{bm-disable-all}`[ch5_code/src/global_alignment/GlobalMultipleAlignment_Matrix.py](ch5_code/src/global_alignment/GlobalMultipleAlignment_Matrix.py) (lines 12 to 79):`{bm-enable-all}`

```python
def generate_matrix(seq_node_counts: List[int]) -> List[Any]:
    last_buffer = [[-1.0, (None, None), '?'] for _ in range(seq_node_counts[-1])]  # row
    for dim in reversed(seq_node_counts[:-1]):
        # DON'T USE DEEPCOPY -- VERY SLOW: https://stackoverflow.com/a/29385667
        # last_buffer = [deepcopy(last_buffer) for _ in range(dim)]
        last_buffer = [pickle.loads(pickle.dumps(last_buffer, -1)) for _ in range(dim)]
    return last_buffer


def get_cell(matrix: List[Any], idxes: Iterable[int]):
    buffer = matrix
    for i in idxes:
        buffer = buffer[i]
    return buffer


def set_cell(matrix: List[Any], idxes: Iterable[int], value: Any):
    buffer = matrix
    for i in idxes[:-1]:
        buffer = buffer[i]
    buffer[idxes[-1]] = value


def backtrack(
        node_matrix: List[List[Any]],
        dimensions: List[int]
) -> Tuple[float, List[Tuple[ELEM, ELEM]]]:
    node_idxes = [d - 1 for d in dimensions]
    final_weight = get_cell(node_matrix, node_idxes)[0]
    alignment = []
    while set(node_idxes) != {0}:
        _, elems, backtrack_ptr = get_cell(node_matrix, node_idxes)
        node_idxes = backtrack_ptr
        alignment.append(elems)
    return final_weight, alignment[::-1]


def global_alignment(
        seqs: List[List[ELEM]],
        weight_lookup: WeightLookup
) -> Tuple[float, List[Tuple[ELEM, ...]]]:
    seq_node_counts = [len(s) + 1 for s in seqs]
    node_matrix = generate_matrix(seq_node_counts)
    src_node = get_cell(node_matrix, [0] * len(seqs))
    src_node[0] = 0.0                   # source node weight
    src_node[1] = (None, ) * len(seqs)  # source node elements (elements don't matter for source node)
    src_node[2] = (None, ) * len(seqs)  # source node parent (direction doesn't matter for source node)
    for to_node in product(*(range(sc) for sc in seq_node_counts)):
        parents = []
        parent_idx_ranges = []
        for idx in to_node:
            vals = [idx]
            if idx > 0:
                vals += [idx-1]
            parent_idx_ranges.append(vals)
        for from_node in product(*parent_idx_ranges):
            if from_node == to_node:  # we want indexes of parent nodes, not self
                continue
            edge_elems = tuple(None if f == t else s[t-1] for s, f, t in zip(seqs, from_node, to_node))
            parents.append([
                get_cell(node_matrix, from_node)[0] + weight_lookup.lookup(*edge_elems),
                edge_elems,
                from_node
            ])
        if parents:  # parents will be empty if source node
            set_cell(node_matrix, to_node, max(parents, key=lambda x: x[0]))
    return backtrack(node_matrix, seq_node_counts)
```