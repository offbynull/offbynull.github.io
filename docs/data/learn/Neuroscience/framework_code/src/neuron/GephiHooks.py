from collections import defaultdict
from typing import Any

from actor_framework.Actor import Actor
from actor_framework.Address import Address
from actor_framework.Context import Context
from gephi_interface.GephiGraph import GephiGraph
from neuron.EnergySupplierActor import EnergySupplierActor
from neuron.SomaActor import SomaActor
from neuron.SynapseActor import SynapseActor


class GephiHooks:
    def __init__(self):
        self.gg = GephiGraph()
        self.gg.__enter__()
        self.edges = defaultdict(set)

    def _added_introspection_hook(self, addr: Address, actor: Actor):
        if isinstance(actor, SomaActor):
            n = self.gg.get_node(str(addr)) if self.gg.has_node(str(addr)) else self.gg.new_node(str(addr))
            self.gg.get_node(str(addr)).update_color(1.0, 0.0, 0.0)
            n.update_size(4.0)
            self.gg.commit()
        elif isinstance(actor, SynapseActor):
            n = self.gg.get_node(str(addr)) if self.gg.has_node(str(addr)) else self.gg.new_node(str(addr))
            n.update_size(1.0)
            n.update_color(0.0, 0.0, 1.0)
            self.gg.new_edge(str(actor.from_soma), str(addr))
            self.gg.new_edge(str(addr), str(actor.to_dendrite_or_soma))
            self.gg.commit()
        elif isinstance(actor, EnergySupplierActor):
            n = self.gg.get_node(str(addr)) if self.gg.has_node(str(addr)) else self.gg.new_node(str(addr))
            n.update_size(0.5)
            n.update_color(0.0, 1.0, 0.0)
            for soma_addr in actor.soma_addresses:
                self.gg.new_edge(str(addr), str(soma_addr))
            self.gg.commit()

    def _removed_introspection_hook(self, addr: Address, actor: Actor):
        self.gg.get_node(str(addr)).delete()
        self.gg.commit()

    def _post_exec_introspection_hook(self, addr: Address, actor: Actor, ctx: Context, msg: Any):
        if isinstance(actor, SomaActor):
            self.gg.get_node(str(addr)).update_color(actor.energy_buildup / 100, 0.0, 0.0)
            self.gg.commit()


    @property
    def added_introspection_hook(self):
        return lambda addr, actor: self._added_introspection_hook(addr, actor)

    @property
    def removed_introspection_hook(self):
        return lambda addr, actor: self._removed_introspection_hook(addr, actor)

    @property
    def post_exec_introspection_hook(self):
        return lambda addr, actor, ctx, msg: self._post_exec_introspection_hook(addr, actor, ctx, msg)
