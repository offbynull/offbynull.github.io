from abc import ABC, abstractmethod
from typing import TypeVar, Generic

T = TypeVar('T')


class IdGenerator(ABC, Generic[T]):
    @abstractmethod
    def __next__(self) -> T:
        ...

    def next_id(self) -> T:
        return next(self)


class IntegerIdGenerator(IdGenerator[int]):
    def __init__(self, start_count: int = 0):
        self.start_count = start_count

    def __next__(self) -> int:
        ret = self.start_count
        self.start_count += 1
        return ret


class StringIdGenerator(IdGenerator[str]):
    def __init__(self, prefix: str, start_count: int = 0):
        self.prefix = prefix
        self.start_count = start_count

    def __next__(self) -> str:
        ret = self.start_count
        self.start_count += 1
        return f'{self.prefix}{ret}'
