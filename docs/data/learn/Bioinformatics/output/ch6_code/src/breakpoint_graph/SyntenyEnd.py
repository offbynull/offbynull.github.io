from __future__ import annotations

from enum import Enum


# MARKDOWN
class SyntenyEnd(Enum):
    HEAD = 'h'
    TAIL = 't'
# MARKDOWN

    def swap(self) -> SyntenyEnd:
        if self == SyntenyEnd.HEAD:
            return SyntenyEnd.TAIL
        else:
            return SyntenyEnd.HEAD

    def __lt__(self, other):
        return self.value < other.value
