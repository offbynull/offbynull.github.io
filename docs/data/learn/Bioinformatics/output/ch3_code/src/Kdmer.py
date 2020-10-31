from __future__ import annotations


class Kdmer:
    def __init__(self: Kdmer, prefix: str, suffix: str, d: int):
        assert len(prefix) == len(suffix)
        self._head = prefix
        self._tail = suffix
        self._d = d
        self._k = len(prefix)

    @property
    def head(self: Kdmer) -> str:
        return self._head

    @property
    def tail(self: Kdmer) -> str:
        return self._tail

    @property
    def d(self: Kdmer) -> int:
        return self._d

    @property
    def k(self: Kdmer) -> int:
        return self._k

    def __eq__(self, o: Kdmer) -> bool:
        return type(self) is type(o) and self._head == o._head and self._tail == o._tail and self._d == o._d

    def __hash__(self) -> int:
        return hash((self._head, self._tail, self._d))

    def __str__(self):
        return str(self._head) + ('-' * self._d) + str(self._tail)

    def __repr__(self):
        return str(self)