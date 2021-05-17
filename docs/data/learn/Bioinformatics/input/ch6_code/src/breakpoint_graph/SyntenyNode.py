from __future__ import annotations

from BreakpointGraph import SyntenyEnd


# MARKDOWN
class SyntenyNode:
    def __init__(self, id: str, end: SyntenyEnd):
        self.id = id
        self.end = end
# MARKDOWN

    def swap_end(self) -> SyntenyNode:
        return SyntenyNode(self.id, self.end.swap())

    def __lt__(self, other):
        if self.id < other.id:
            return True
        elif self.id == other.id and self.end < other.end:
            return True
        else:
            return False

    def __eq__(self, other):
        if isinstance(other, SyntenyNode):
            return self.id == other.id and self.end == other.end
        else:
            return False

    def __hash__(self):
        return hash((self.id, self.end))

    def __str__(self):
        return f'{self.id}_{self.end.value}'

    def __repr__(self):
        return str(self)
