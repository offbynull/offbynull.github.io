`{bm-disable-all}`[ch6_code/src/breakpoint_graph/ColoredEdge.py](ch6_code/src/breakpoint_graph/ColoredEdge.py) (lines 46 to 86):`{bm-enable-all}`

```python
# Takes e1 and e2 and swaps the ends, such that one of the swapped edges becomes desired_e. That is, e1 should have
# an end matching one of desired_e's ends while e2 should have an end matching desired_e's other end.
#
# This is basically a 2-break.
@staticmethod
def swap_ends(
        e1: Optional[ColoredEdge],
        e2: Optional[ColoredEdge],
        desired_e: ColoredEdge
) -> Optional[ColoredEdge]:
    if e1 is None and e2 is None:
        raise ValueError('Both edges can\'t be None')
    if TerminalNode.INST in desired_e:
        # In this case, one of desired_e's ends is TERM (they can't both be TERM). That means either e1 or e2 will
        # be None because there's only one valid end (non-TERM end) to swap with.
        _e = next(filter(lambda x: x is not None, [e1, e2]), None)
        if _e is None:
            raise ValueError('If the desired edge has a terminal node, one of the edges must be None')
        if desired_e.non_term() not in {_e.n1, _e.n2}:
            raise ValueError('Unexpected edge node(s) encountered')
        if desired_e == _e:
            raise ValueError('Edge is already desired edge')
        other_n1 = _e.other_end(desired_e.non_term())
        other_n2 = TerminalNode.INST
        return ColoredEdge(other_n1, other_n2)
    else:
        # In this case, neither of desired_e's ends is TERM. That means both e1 and e2 will be NOT None.
        if desired_e in {e1, e2}:
            raise ValueError('Edge is already desired edge')
        if desired_e.n1 in e1 and desired_e.n2 in e2:
            other_n1 = e1.other_end(desired_e.n1)
            other_n2 = e2.other_end(desired_e.n2)
        elif desired_e.n1 in e2 and desired_e.n2 in e1:
            other_n1 = e2.other_end(desired_e.n1)
            other_n2 = e1.other_end(desired_e.n2)
        else:
            raise ValueError('Unexpected edge node(s) encountered')
        if {other_n1, other_n2} == {TerminalNode.INST}:  # if both term edges, there is no other edge
            return None
        return ColoredEdge(other_n1, other_n2)
```