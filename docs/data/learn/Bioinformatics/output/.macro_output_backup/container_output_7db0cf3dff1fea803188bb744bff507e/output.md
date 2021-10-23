`{bm-disable-all}`[ch6_code/src/breakpoint_graph/Permutation.py](ch6_code/src/breakpoint_graph/Permutation.py) (lines 111 to 146):`{bm-enable-all}`

```python
def to_colored_edges(self) -> List[ColoredEdge]:
    ret = []
    # add link to dummy head if linear
    if not self.cyclic:
        b = self.blocks[0]
        ret.append(
            ColoredEdge(TerminalNode.INST, b.to_synteny_edge().n1)
        )
    # add normal edges
    for (b1, b2), idx in slide_window(self.blocks, 2, cyclic=self.cyclic):
        if b1.dir == Direction.BACKWARD and b2.dir == Direction.FORWARD:
            n1 = SyntenyNode(b1.id, SyntenyEnd.HEAD)
            n2 = SyntenyNode(b2.id, SyntenyEnd.HEAD)
        elif b1.dir == Direction.FORWARD and b2.dir == Direction.BACKWARD:
            n1 = SyntenyNode(b1.id, SyntenyEnd.TAIL)
            n2 = SyntenyNode(b2.id, SyntenyEnd.TAIL)
        elif b1.dir == Direction.FORWARD and b2.dir == Direction.FORWARD:
            n1 = SyntenyNode(b1.id, SyntenyEnd.TAIL)
            n2 = SyntenyNode(b2.id, SyntenyEnd.HEAD)
        elif b1.dir == Direction.BACKWARD and b2.dir == Direction.BACKWARD:
            n1 = SyntenyNode(b1.id, SyntenyEnd.HEAD)
            n2 = SyntenyNode(b2.id, SyntenyEnd.TAIL)
        else:
            raise ValueError('???')
        ret.append(
            ColoredEdge(n1, n2)
        )
    # add link to dummy tail if linear
    if not self.cyclic:
        b = self.blocks[-1]
        ret.append(
            ColoredEdge(b.to_synteny_edge().n2, TerminalNode.INST)
        )
    # return
    return ret
```