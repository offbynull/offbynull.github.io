from actor_framework.Actor import Actor
from actor_framework.Address import Address
from actor_framework.Context import Context


class EnergySupplierActor(Actor):
    def __init__(self, soma_addresses: set[Address], energy_per_tick: int, tick: int):
        self.soma_addresses = soma_addresses
        self.energy_per_tick = energy_per_tick
        self.tick = tick

    def step(self, ctx: Context):
        while True:
            from_addr, to_addr, msg = ctx.get_incoming_message()
            match msg:
                case 'SUPPLY':
                    for addr in self.soma_addresses:
                        ctx.add_outgoing_message(addr, ('INCREASE_ENERGY', self.energy_per_tick))
                    ctx.add_outgoing_message(from_addr, 'SUPPLY', wait_duration_override=self.tick)
            yield
