from actor_framework.Actor import Actor
from actor_framework.Address import Address
from actor_framework.Context import Context


class SynapseActor(Actor):
    def __init__(self, from_soma: Address, to_dendrite_or_soma: Address):
        self.from_soma = from_soma
        self.to_dendrite_or_soma = to_dendrite_or_soma

    def step(self, ctx: Context) -> None:
        from_addr, to_addr, msg = ctx.get_incoming_message()
        if from_addr != self.from_soma or self.to_dendrite_or_soma != to_addr:
            return
        if msg == 'ACTION_POTENTIAL':
            ctx.add_outgoing_message(self.to_dendrite_or_soma, 'ENERGY_RELEASE')
