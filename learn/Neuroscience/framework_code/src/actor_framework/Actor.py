from abc import ABC, abstractmethod
from typing import Generator

from actor_framework.Context import Context


class Actor(ABC):
    @abstractmethod
    def step(self, ctx: Context) -> Generator[None, None, None]:
        raise NotImplementedError()
