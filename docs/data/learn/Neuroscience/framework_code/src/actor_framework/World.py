import heapq
from typing import Any, Callable

from actor_framework.Actor import Actor
from actor_framework.Address import Address
from actor_framework.Context import Context


class World:
    def __init__(
            self,
            duration_calculator: Callable[[Address, Address, Any], int]
    ):
        self.actors = {}
        self.timestamp = 0
        self.duration_calculator = duration_calculator
        self.step_queue = []

    def add_actor(
            self,
            addr: Address | str,
            actor: Actor | Callable[[Context], None],
            priming_msg: Any | None = None
    ) -> None:
        if isinstance(addr, str):
            addr = Address.from_string(addr)
        if addr in self.actors:
            raise ValueError()
        if isinstance(actor, Actor):
            self.actors[addr] = actor
        else:
            class FakeActor:
                def step(self, ctx):
                    actor(ctx)
            self.actors[addr] = FakeActor()
        if priming_msg is not None:
            duration = self.duration_calculator(addr, addr, priming_msg)
            timestamp = self.timestamp + duration
            heapq.heappush(self.step_queue, (timestamp, addr, addr, priming_msg))

    def step(self):
        if not self.step_queue:
            return
        timestamp, from_addr, to_addr, msg = heapq.heappop(self.step_queue)
        assert timestamp >= self.timestamp
        self.timestamp = timestamp
        if to_addr not in self.actors:
            return
        ctx = Context(timestamp, from_addr, from_addr, to_addr, msg)
        actor = self.actors[to_addr]
        actor.step(ctx)
        for from_addr, to_addr, msg, duration in ctx._out_msgs:
            if duration is None:
                duration = self.duration_calculator(from_addr, to_addr, msg)
            timestamp = self.timestamp + duration
            heapq.heappush(self.step_queue, (timestamp, from_addr, to_addr, msg))
        return



if __name__ == '__main__':
    w = World(lambda src, dst, msg: 1)
    w.add_actor('test:a', lambda ctx: print(f'{ctx.get_incoming_message()}'), 'hello world!')
    w.step()
    w.step()
    w.step()
