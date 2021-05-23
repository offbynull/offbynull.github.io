`{bm-disable-all}`[ch6_code/src/breakpoint_graph/ColoredEdge.py](ch6_code/src/breakpoint_graph/ColoredEdge.py) (lines 11 to 29):`{bm-enable-all}`

```python
class ColoredEdge:
    def __init__(
            self,
            n1: Union[SyntenyNode, TerminalNode],
            n2: Union[SyntenyNode, TerminalNode]
    ):
        assert isinstance(n1, SyntenyNode) or isinstance(n2, SyntenyNode), 'Both ends cant\'t be at terminal node'
        assert n1 != n2, 'Both ends can\'t be equal'
        # sort such that nodes are always placed in the same order
        if isinstance(n1, SyntenyNode) and isinstance(n2, SyntenyNode):  # order pair so n1 is always smallest
            x = [n1, n2]
            x.sort()
            n1 = x[0]
            n2 = x[1]
        elif isinstance(n2, TerminalNode):  # one is term node? n1 should be the term node
            n1, n2 = n2, n1
        self.n1 = n1
        self.n2 = n2
```