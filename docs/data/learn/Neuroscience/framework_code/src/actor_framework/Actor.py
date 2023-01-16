from abc import ABC, abstractmethod

from actor_framework.Context import Context


class Actor(ABC):
    @abstractmethod
    def step(self, ctx: Context) -> None:
        raise NotImplementedError()
