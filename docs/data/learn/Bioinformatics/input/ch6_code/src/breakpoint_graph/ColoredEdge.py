from __future__ import annotations

from typing import Union, Optional

from breakpoint_graph.SyntenyEnd import SyntenyEnd
from breakpoint_graph.SyntenyNode import SyntenyNode
from breakpoint_graph.TerminalNode import TerminalNode


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

    def other_end(self, n: Union[SyntenyNode, TerminalNode]):
        if n == self.n1:
            return self.n2
        elif n == self.n2:
            return self.n1
        else:
            raise ValueError('???')

    def non_term(self):
        return self.other_end(TerminalNode.INST)

    def has_term(self):
        return isinstance(self.n1, TerminalNode) or self.n2 is isinstance(self.n2, TerminalNode)

    # Takes e1 and e2 and swaps the ends, such that one of the swapped edges becomes desired_e. That is, e1 should have
    # an end matching one of desired_e's ends while e2 should have an end matching desired_e's other end.
    #
    # This is basically a 2-break. The e1
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

    def __eq__(self, other):
        return self.n1 == other.n1 and self.n2 == other.n2

    def __hash__(self):
        return hash((self.n1, self.n2))

    def __str__(self):
        return str((self.n1, self.n2))

    def __repr__(self):
        return str(self)

    def __contains__(self, item: Union[SyntenyNode, TerminalNode]):
        return self.n1 == item or self.n2 == item


if __name__ == '__main__':
    e = ColoredEdge.swap_ends(
        e1=ColoredEdge(SyntenyNode('C', SyntenyEnd.HEAD), TerminalNode.INST),
        e2=ColoredEdge(SyntenyNode('C', SyntenyEnd.TAIL), SyntenyNode('D', SyntenyEnd.HEAD)),
        desired_e=ColoredEdge(SyntenyNode('C', SyntenyEnd.HEAD), SyntenyNode('D', SyntenyEnd.HEAD))
    )
    print(f'{e}')
    e = ColoredEdge.swap_ends(
        e1=ColoredEdge(SyntenyNode('C', SyntenyEnd.TAIL), SyntenyNode('D', SyntenyEnd.HEAD)),
        e2=ColoredEdge(SyntenyNode('C', SyntenyEnd.HEAD), TerminalNode.INST),
        desired_e=ColoredEdge(SyntenyNode('C', SyntenyEnd.HEAD), SyntenyNode('D', SyntenyEnd.HEAD))
    )
    print(f'{e}')
    e = ColoredEdge.swap_ends(
        e1=ColoredEdge(SyntenyNode('D', SyntenyEnd.HEAD), SyntenyNode('D', SyntenyEnd.TAIL)),
        e2=None,
        desired_e=ColoredEdge(TerminalNode.INST, SyntenyNode('D', SyntenyEnd.TAIL))
    )
    print(f'{e}')
