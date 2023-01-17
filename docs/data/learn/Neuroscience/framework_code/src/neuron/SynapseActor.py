from actor_framework.Actor import Actor
from actor_framework.Address import Address
from actor_framework.Context import Context


class SynapseActor(Actor):
    def __init__(self, from_soma: Address, to_dendrite_or_soma: Address):
        self.from_soma = from_soma
        self.to_dendrite_or_soma = to_dendrite_or_soma

    def step(self, ctx: Context):
        while True:
            from_addr, to_addr, msg = ctx.get_incoming_message()
            if msg == 'ACTION_POTENTIAL' and from_addr == self.from_soma or self.to_dendrite_or_soma == to_addr:
                ctx.add_outgoing_message(self.to_dendrite_or_soma, 'ENERGY_RELEASE')
            yield
