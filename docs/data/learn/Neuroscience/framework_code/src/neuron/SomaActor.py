from actor_framework.Actor import Actor
from actor_framework.Context import Context


class SomaActor(Actor):
    def __init__(self):
        self.energy_buildup = 50

    def step(self, ctx: Context):
        while True:
            from_addr, to_addr, msg = ctx.get_incoming_message()
            if msg == 'DECREASE_ENERGY':
                self.energy_buildup = max(0, self.energy_buildup - 1)
                print(f'{self.energy_buildup=} {ctx.get_timestamp()=}')
                ctx.add_outgoing_message(to_addr, 'DECREASE_ENERGY', wait_duration_override=1)
            yield
