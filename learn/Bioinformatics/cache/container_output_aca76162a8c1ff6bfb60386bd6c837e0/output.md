`{bm-disable-all}`[ch6_code/src/breakpoint_graph/ColoredEdgeSet.py](ch6_code/src/breakpoint_graph/ColoredEdgeSet.py) (lines 16 to 35):`{bm-enable-all}`

```python
# Represents a single genome in a breakpoint graph
class ColoredEdgeSet:
    def __init__(self):
        self.by_node: Dict[SyntenyNode, ColoredEdge] = {}

    @staticmethod
    def create(ce_list: Iterable[ColoredEdge]) -> ColoredEdgeSet:
        ret = ColoredEdgeSet()
        for ce in ce_list:
            ret.insert(ce)
        return ret

    def insert(self, e: ColoredEdge):
        if e.n1 in self.by_node or e.n2 in self.by_node:
            raise ValueError(f'Node already occupied: {e}')
        if not isinstance(e.n1, TerminalNode):
            self.by_node[e.n1] = e
        if not isinstance(e.n2, TerminalNode):
            self.by_node[e.n2] = e
```