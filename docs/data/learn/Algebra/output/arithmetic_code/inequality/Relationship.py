from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from expression.parser.Parser import Node
from expression.parser.Printer import to_string


class Relation(Enum):
    LT = '<'
    # LTE = '<='
    GT = '>'
    # GTE = '>='
    EQ = '='

    def __str__(self):
        return self.value

    def swap(self):
        if self == Relation.LT:
            return Relation.GT
        # elif self == Relation.LTE:
        #     return Relation.GTE
        elif self == Relation.GT:
            return Relation.LT
        # elif self == Relation.GT:
        #     return Relation.GTE
        elif self == Relation.EQ:
            return Relation.EQ
        raise ValueError('???')

    # def includes_equality(self):
    #     return self == Relation.LTE or self == Relation.GTE


@dataclass(frozen=True)
class Relationship:
    lhs: Node
    relation: Relation
    rhs: Node

    def __str__(self):
        return f'{to_string(self.lhs)} {self.relation} {to_string(self.rhs)}'


@dataclass(frozen=True)
class ConditionalRelationship:
    relationship: Relationship
    conditions: frozenset[Relationship]

    def __str__(self):
        ret = f'{self.relationship}'
        if self.conditions:
            ret += ', if ' + ' | '.join(str(c) for c in self.conditions)
        return ret


