`{bm-disable-all}`[ch6_code/src/breakpoint_graph/Permutation.py](ch6_code/src/breakpoint_graph/Permutation.py) (lines 158 to 196):`{bm-enable-all}`

```python
@staticmethod
def from_colored_edges(
        colored_edges: ColoredEdgeSet,
        start_n: SyntenyNode,
        cyclic: bool
) -> Tuple[Permutation, Set[ColoredEdge]]:
    # if not cyclic, it's expected that start_n is either from or to a term node
    if not cyclic:
        ce = colored_edges.find(start_n)
        assert ce.has_term(), "Start node must be for a terminal colored edge"
    # if cyclic stop once you detect a loop, otherwise  stop once you encounter a term node
    if cyclic:
        walked = set()
        def stop_test(x):
            ret = x in walked
            walked.add(next_n)
            return ret
    else:
        def stop_test(x):
            return x == TerminalNode.INST
    # begin loop
    blocks = []
    start_ce = colored_edges.find(start_n)
    walked_ce_set = {start_ce}
    next_n = start_n
    while not stop_test(next_n):
        if next_n.end == SyntenyEnd.HEAD:
            b = Block(Direction.FORWARD, next_n.id)
        elif next_n.end == SyntenyEnd.TAIL:
            b = Block(Direction.BACKWARD, next_n.id)
        else:
            raise ValueError('???')
        blocks.append(b)
        swapped_n = next_n.swap_end()
        next_ce = colored_edges.find(swapped_n)
        next_n = next_ce.other_end(swapped_n)
        walked_ce_set.add(next_ce)
    return Permutation(blocks, cyclic), walked_ce_set
```