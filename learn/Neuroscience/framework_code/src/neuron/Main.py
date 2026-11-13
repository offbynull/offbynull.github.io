from random import sample, choice
from typing import Any

from actor_framework.Actor import Actor
from actor_framework.Address import Address
from actor_framework.World import World
from neuron.EnergySupplierActor import EnergySupplierActor
from neuron.GephiHooks import GephiHooks
from neuron.SomaActor import SomaActor
from neuron.SynapseActor import SynapseActor


def create_neuron(id: int, recving_ids: set[int]) -> list[tuple[Address, Actor, Any]]:
    actors = []
    synapse_addresses = set()
    for recving_id in recving_ids:
        synapse_address = Address.from_string(f'synapse_{id}_{recving_id}')
        synapse_actor = SynapseActor(Address.from_string(f'soma_{id}'), Address.from_string(f'soma_{recving_id}'))
        synapse_priming_msg = None
        actors.append((synapse_address, synapse_actor, synapse_priming_msg))
        synapse_addresses.add(synapse_address)
    actors.append((Address.from_string(f'soma_{id}'), SomaActor(synapse_addresses), 'DECREASE_ENERGY'))
    return actors


def create_electrical_suppliers(id: int, recving_ids: set[int], energy_per_tick: int, tick: int) -> tuple[Address, Actor, Any]:
    soma_addresses = set()
    for recving_id in recving_ids:
        soma_address = Address.from_string(f'soma_{recving_id}')
        soma_addresses.add(soma_address)
    return Address.from_string(f'nrg_{id}'), EnergySupplierActor(soma_addresses, energy_per_tick, tick), 'SUPPLY'


def create_neurons(
        w: World,
        count: int,
        neighbour_conn_amount_minmax: tuple[int, int],
        neighbour_conn_range_minmax: tuple[int, int],
        non_neighbour_conn_amount_minmax: tuple[int, int]
):
    for i in range(count):
        neighbour_conn_amount = choice(range(*neighbour_conn_amount_minmax))
        neighbour_conn_range_min = i + neighbour_conn_range_minmax[0]
        neighbour_conn_range_max = i + neighbour_conn_range_minmax[1]
        neighbour_conns = sample(
            [x % count for x in range(neighbour_conn_range_min, neighbour_conn_range_max)],
            neighbour_conn_amount
        )
        non_neighbour_conn_amount = choice(range(*non_neighbour_conn_amount_minmax))
        non_neighbour_conns = sample(range(0, count), non_neighbour_conn_amount)
        all_conns = set(neighbour_conns + non_neighbour_conns)
        actors = create_neuron(i, all_conns)
        for actor_addr, actor, priming_msg in actors:
            w.add_actor(actor_addr, actor, priming_msg)


if __name__ == '__main__':
    gephi_hooks = GephiHooks()
    w = World(
        added_introspection_hook=gephi_hooks.added_introspection_hook,
        removed_introspection_hook=gephi_hooks.removed_introspection_hook,
        post_exec_introspection_hook=gephi_hooks.post_exec_introspection_hook
    )
    create_neurons(
        w,
        1000,
        (2, 10),    # neighbour count
        (-10, 10),  # neighbour range (-/+ what window is considered a neighbour)
        (2, 10)     # non-neighbour count
    )
    for i in range(10):
        addr, actor, priming_msg = create_electrical_suppliers(i, set(sample(range(0, 1000), 20)), i, 1)
        w.add_actor(addr, actor, priming_msg)

    print('Running...')
    while True:
        w.step()
