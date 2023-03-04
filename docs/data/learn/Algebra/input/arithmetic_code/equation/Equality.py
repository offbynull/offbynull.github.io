from dataclasses import dataclass
from enum import Enum

from expression.parser.Parser import Node
from expression.parser.Printer import to_string


@dataclass(frozen=True)
class Equality:
    lhs: Node
    rhs: Node

    def __str__(self):
        return f'{to_string(self.lhs)} = {to_string(self.rhs)}'
