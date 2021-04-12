from __future__ import annotations

from typing import Optional

from BreakpointGraph import SyntenyEnd


class Node:
    def __init__(self, id: Optional[str], end: SyntenyEnd):
        self.id = id
        self.end = end

    def other_end(self) -> Node:
        return Node(self.id, self.end.swap())

    def __lt__(self, other):
        if self.id < other.id:
            return True
        elif self.id == other.id and self.end < other.end:
            return True
        else:
            return False

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.id == other.id and self.end == other.end
        else:
            return False

    def __hash__(self):
        return hash((self.id, self.end))

    def __str__(self):
        return str((self.id, self.end))

    def __repr__(self):
        return str(self)