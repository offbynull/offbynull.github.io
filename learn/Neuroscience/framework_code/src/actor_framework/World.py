import heapq
from typing import Any, Callable

from actor_framework.Actor import Actor
from actor_framework.Address import Address
from actor_framework.Context import Context


class World:
    def __init__(
            self,
            duration_calculator: Callable[[Address, Address, Any], int] | None = None,
            added_introspection_hook: Callable[[Address, Actor], None] | None = None,
            pre_exec_introspection_hook: Callable[[Address, Actor, Context, Any], None] | None = None,
            post_exec_introspection_hook: Callable[[Address, Actor, Context, Any], None] | None = None,
            removed_introspection_hook: Callable[[Address, Actor], None] | None = None
    ):
        self.actors = {}
        self.timestamp = 0
        if duration_calculator is None:
            self.duration_calculator = lambda src, dst, msg: 0
        else:
            self.duration_calculator = duration_calculator
        if added_introspection_hook is None:
            self.added_introspection_hook = lambda addr, actor: None
        else:
            self.added_introspection_hook = added_introspection_hook
        if removed_introspection_hook is None:
            self.removed_introspection_hook = lambda addr, actor: None
        else:
            self.removed_introspection_hook = removed_introspection_hook
        if pre_exec_introspection_hook is None:
            self.pre_exec_introspection_hook = lambda addr, actor, ctx, priming_msg: None
        else:
            self.pre_exec_introspection_hook = pre_exec_introspection_hook
        if post_exec_introspection_hook is None:
            self.post_exec_introspection_hook = lambda addr, actor, ctx, priming_msg: None
        else:
            self.post_exec_introspection_hook = post_exec_introspection_hook
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
        ctx = Context(addr)
        if not isinstance(actor, Actor):
            _actor_func = actor
            class FakeActor:
                def step(self, ctx):
                    while True:
                        _actor_func(ctx)
                        yield
            actor = FakeActor()
        self.actors[addr] = actor, actor.step(ctx), ctx
        self.added_introspection_hook(addr, actor)
        if priming_msg is not None:
            duration = self.duration_calculator(addr, addr, priming_msg)
            timestamp = self.timestamp + duration
            heapq.heappush(self.step_queue, (timestamp, addr, addr, priming_msg))

    def get_actors(self) -> dict[Address, Actor]:
        return {addr: obj for addr, (obj, _, _) in self.actors.items()}

    def step(self) -> int | None:
        if not self.step_queue:
            return None
        timestamp, from_addr, to_addr, msg = heapq.heappop(self.step_queue)
        assert timestamp >= self.timestamp
        self.timestamp = timestamp
        if to_addr not in self.actors:
            return None
        actor_obj, actor_generator, ctx = self.actors[to_addr]
        ctx._update(timestamp, from_addr, to_addr, msg)
        try:
            self.pre_exec_introspection_hook(ctx._self_addr, actor_obj, ctx, msg)
            next(actor_generator)
            self.post_exec_introspection_hook(ctx._self_addr, actor_obj, ctx, msg)
        except StopIteration:
            del self.actors[ctx._self_addr]
            self.removed_introspection_hook(ctx._self_addr, actor_obj)
        current_timestamp = timestamp
        for from_addr, to_addr, msg, duration in ctx._out_msgs:
            if duration is None:
                duration = self.duration_calculator(from_addr, to_addr, msg)
            timestamp = self.timestamp + duration
            heapq.heappush(self.step_queue, (timestamp, from_addr, to_addr, msg))
        return current_timestamp

    def next_timestamp(self) -> int | None:
        if len(self.step_queue) == 0:
            return None
        timestamp, from_addr, to_addr, msg = heapq.heappop(self.step_queue)
        heapq.heappush(self.step_queue, (timestamp, from_addr, to_addr, msg))
        return timestamp



if __name__ == '__main__':
    w = World(lambda src, dst, msg: 1)
    w.add_actor('test:a', lambda ctx: print(f'{ctx.get_incoming_message()}'), 'hello world!')
    w.step()
    w.step()
    w.step()
