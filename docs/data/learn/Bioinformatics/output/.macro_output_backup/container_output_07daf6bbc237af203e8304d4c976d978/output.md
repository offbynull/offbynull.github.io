`{bm-disable-all}`[ch6_code/src/breakpoint_graph/SyntenyEdge.py](ch6_code/src/breakpoint_graph/SyntenyEdge.py) (lines 10 to 16):`{bm-enable-all}`

```python
class SyntenyEdge:
    def __init__(self, n1: SyntenyNode, n2: SyntenyNode):
        assert n1.id == n2.id
        assert n1.end != n2.end
        self.n1 = n1
        self.n2 = n2
```