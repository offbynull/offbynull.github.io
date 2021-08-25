`{bm-disable-all}`[ch3_code/src/ToDeBruijnGraph.py](ch3_code/src/ToDeBruijnGraph.py) (lines 13 to 20):`{bm-enable-all}`

```python
def to_debruijn_graph(reads: List[T], skip: int = 1) -> Graph[T]:
    graph = Graph()
    for read in reads:
        from_node = read.prefix(skip)
        to_node = read.suffix(skip)
        graph.insert_edge(from_node, to_node)
    return graph
```