`{bm-disable-all}`[ch6_code/src/breakpoint_graph/ColoredEdgeSet.py](ch6_code/src/breakpoint_graph/ColoredEdgeSet.py) (lines 80 to 126):`{bm-enable-all}`

```python
# Walks the colored edges, spliced with synteny edges.
def walk(self) -> List[List[Union[ColoredEdge, SyntenyEdge]]]:
    ret = []
    all_edges = self.edges()
    term_edges = set()
    for ce in all_edges:
        if ce.has_term():
            term_edges.add(ce)
    # handle linear chromosomes
    while term_edges:
        ce = term_edges.pop()
        n = ce.non_term()
        all_edges.remove(ce)
        edges = []
        while True:
            se_n1 = n
            se_n2 = se_n1.swap_end()
            se = SyntenyEdge(se_n1, se_n2)
            edges += [ce, se]
            ce = self.by_node[se_n2]
            if ce.has_term():
                edges += [ce]
                term_edges.remove(ce)
                all_edges.remove(ce)
                break
            n = ce.other_end(se_n2)
            all_edges.remove(ce)
        ret.append(edges)
    # handle cyclic chromosomes
    while all_edges:
        start_ce = all_edges.pop()
        ce = start_ce
        n = ce.n1
        edges = []
        while True:
            se_n1 = n
            se_n2 = se_n1.swap_end()
            se = SyntenyEdge(se_n1, se_n2)
            edges += [ce, se]
            ce = self.by_node[se_n2]
            if ce == start_ce:
                break
            n = ce.other_end(se_n2)
            all_edges.remove(ce)
        ret.append(edges)
    return ret
```