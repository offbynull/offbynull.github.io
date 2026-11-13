from actor_framework.Actor import Actor
from actor_framework.Address import Address
from actor_framework.Context import Context


class SomaActor(Actor):
    def __init__(self, synapse_addresses: set[Address]):
        self.energy_buildup = 50.0
        self.synapse_addresses = synapse_addresses

    def step(self, ctx: Context):
        while True:
            from_addr, to_addr, msg = ctx.get_incoming_message()
            match msg:
                case 'DECREASE_ENERGY':
                    self.energy_buildup = max(0, self.energy_buildup - 1)
                    # print(f'{self.energy_buildup=} {ctx.get_timestamp()=}')
                    ctx.add_outgoing_message(to_addr, 'DECREASE_ENERGY', wait_duration_override=1)
                case ('INCREASE_ENERGY', energy):
                    self.energy_buildup = min(100, self.energy_buildup + energy)
                case ('DECREASE_ENERGY', energy):
                    self.energy_buildup = max(0, self.energy_buildup - energy)
            if self.energy_buildup == 100.0:
                self.energy_buildup = 50.0
                for synapse_addr in self.synapse_addresses:
                    ctx.add_outgoing_message(synapse_addr, 'ACTION_POTENTIAL')
            yield
