from __future__ import annotations

from dataclasses import dataclass

from expression.Node import Node


def opposite(op: str) -> str:
    if op == '<':
        return '>='
    elif op == '>':
        return '<='
    elif op == '<=':
        return '>'
    elif op == '>=':
        return '<'
    elif op == '=':
        return '='
    raise ValueError('???')


def includes_equality(op: str):
    return op in {'>=', '<=', '='}


@dataclass(frozen=True)
class Relation:
    op: str
    lhs: Node
    rhs: Node

    def __str__(self):
        ret = f'{self.op}({self.lhs},{self.rhs})'
        return ret


@dataclass(frozen=True)
class RelationWithDomain:
    relation: Relation
    domains: frozenset[Relation]
