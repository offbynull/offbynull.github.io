from sys import stdin
from typing import TypeVar, Iterator, Protocol, Any

import yaml

from graph.DirectedGraph import Graph

STATE = TypeVar('STATE')
SYMBOL = TypeVar('SYMBOL')
TRANSITION = tuple[STATE, STATE]


class HmmNodeData(Protocol[SYMBOL]):
    def get_symbol_emission_probability(self, symbol: SYMBOL) -> float:
        ...

    def set_symbol_emission_probability(self, symbol: SYMBOL, probability: float) -> None:
        ...

    def list_symbol_emissions(self) -> Iterator[tuple[SYMBOL, float]]:
        ...

    def is_emittable(self) -> bool:
        ...


class HmmEdgeData(Protocol):
    def get_transition_probability(self) -> float:
        ...

    def set_transition_probability(self, probability: float):
        ...


class BaseHmmNodeData:
    def __init__(self, emission_probabilities: dict[SYMBOL, float]):
        self.emission_probabilities = emission_probabilities

    def get_symbol_emission_probability(self, symbol: SYMBOL) -> float:
        return self.emission_probabilities[symbol]

    def set_symbol_emission_probability(self, symbol: SYMBOL, probability: float) -> None:
        self.emission_probabilities[symbol] = probability

    def list_symbol_emissions(self) -> Iterator[tuple[SYMBOL, float]]:
        return iter(self.emission_probabilities.items())

    def is_emittable(self) -> bool:
        return self.emission_probabilities != {}


class BaseHmmEdgeData:
    def __init__(self, probability: float):
        self.probability = probability

    def get_transition_probability(self) -> float:
        return self.probability

    def set_transition_probability(self, probability: float):
        self.probability = probability


def to_hmm_graph_PRE_PSEUDOCOUNTS(
        transition_probabilities: dict[str, dict[str, float]],
        emission_probabilities: dict[str, dict[str, float]]
) -> Graph[STATE, HmmNodeData, TRANSITION, HmmEdgeData]:
    hmm = Graph()
    for from_state in transition_probabilities:
        if not hmm.has_node(from_state):
            hmm.insert_node(from_state)
        for to_state, weight in transition_probabilities[from_state].items():
            if not hmm.has_node(to_state):
                hmm.insert_node(to_state)
            hmm.insert_edge(
                (from_state, to_state),
                from_state,
                to_state,
                BaseHmmEdgeData(weight)
            )
    for state in emission_probabilities:
        weights = BaseHmmNodeData(emission_probabilities[state])
        if not hmm.has_node(state):
            hmm.insert_node(state)
        hmm.update_node_data(state, weights)
    return hmm


def hmm_to_dot(g: Graph[STATE, HmmNodeData, TRANSITION, HmmEdgeData]) -> str:
    ret = 'digraph G {\n'
    ret += ' graph[rankdir=LR]\n'
    ret += ' node[shape=egg, fontname="Courier-Bold", fontsize=10]\n'
    ret += ' edge[fontname="Courier-Bold", fontsize=10]\n'
    for n in sorted(g.get_nodes()):
        ret += f'"STATE_{n}" [label="{n}"]\n'
    for e in sorted(g.get_edges()):
        n1, n2, data = g.get_edge(e)
        weight = data.get_transition_probability()
        ret += f'"STATE_{n1}" -> "STATE_{n2}" [label="{weight}"]\n'
    added_symbols = set()
    for n in sorted(g.get_nodes()):
        emission_probs = g.get_node_data(n)
        for n_symbol, weight in emission_probs.list_symbol_emissions():
            if n_symbol not in added_symbols:
                ret += f'"SYMBOL_{n_symbol}" [label="{n_symbol}", style="dashed"]\n'
                added_symbols.add(n_symbol)
            ret += f'"STATE_{n}" -> "SYMBOL_{n_symbol}" [label="{weight}", style="dashed"]\n'
    ret += '}'
    return ret


def hmm_add_pseudocounts_to_hidden_state_transition_probabilities(
        hmm: Graph[STATE, HmmNodeData, TRANSITION, HmmEdgeData],
        psuedocount: float
) -> None:
    for from_state in hmm.get_nodes():
        tweaked_transition_weights = {}
        total_transition_probs = 0.0
        for transition in hmm.get_outputs(from_state):
            _, to_state = transition
            prob = hmm.get_edge_data(transition).get_transition_probability() + psuedocount
            tweaked_transition_weights[to_state] = prob
            total_transition_probs += prob
        for to_state, prob in tweaked_transition_weights.items():
            transition = from_state, to_state
            normalized_transition_prob = prob / total_transition_probs
            hmm.get_edge_data(transition).set_transition_probability(normalized_transition_prob)


def hmm_add_pseudocounts_to_symbol_emission_probabilities(
        hmm: Graph[STATE, HmmNodeData, TRANSITION, HmmEdgeData],
        psuedocount: float
) -> None:
    for from_state in hmm.get_nodes():
        tweaked_emission_weights = {}
        total_emission_probs = 0.0
        for symbol, prob in hmm.get_node_data(from_state).list_symbol_emissions():
            prob += psuedocount
            tweaked_emission_weights[symbol] = prob
            total_emission_probs += prob
        for symbol, prob in tweaked_emission_weights.items():
            normalized_transition_prob = prob / total_emission_probs
            hmm.get_node_data(from_state).set_symbol_emission_probability(symbol, normalized_transition_prob)


EXPLODED_NODE_ID = tuple[int, STATE]
EXPLODED_EDGE_ID = tuple[EXPLODED_NODE_ID, EXPLODED_NODE_ID]


def explode_hmm(
        hmm: Graph[STATE, HmmNodeData, TRANSITION, HmmEdgeData],
        hmm_source_n_id: STATE,
        hmm_sink_n_id: STATE,
        emissions: list[SYMBOL]
) -> Graph[EXPLODED_NODE_ID, Any, EXPLODED_EDGE_ID, Any]:
    exploded = Graph()
    # Add exploded source node.
    exploded_source_n_id = -1, hmm_source_n_id
    exploded.insert_node(exploded_source_n_id)
    # Explode out HMM into new graph.
    exploded_from_n_emissions_idx = -1
    exploded_from_n_ids = {exploded_source_n_id}
    exploded_to_n_emissions_idx = 0
    exploded_to_n_ids_emitting = set()
    exploded_to_n_ids_non_emitting = set()
    while exploded_from_n_ids and exploded_to_n_emissions_idx < len(emissions):
        exploded_to_n_symbol = emissions[exploded_to_n_emissions_idx]
        exploded_to_n_ids_emitting = set()
        exploded_to_n_ids_non_emitting = set()
        while exploded_from_n_ids:
            exploded_from_n_id = exploded_from_n_ids.pop()
            _, hmm_from_n_id = exploded_from_n_id
            for _, _, hmm_to_n_id, _ in hmm.get_outputs_full(hmm_from_n_id):
                hmm_to_n_emittable = hmm.get_node_data(hmm_to_n_id).is_emittable()
                if hmm_to_n_emittable:
                    exploded_to_n_id = exploded_to_n_emissions_idx, hmm_to_n_id
                    connect_exploded_nodes(
                        exploded,
                        exploded_from_n_id,
                        exploded_to_n_id,
                        None
                    )
                    exploded_to_n_ids_emitting.add(exploded_to_n_id)
                else:
                    exploded_to_n_id = exploded_from_n_emissions_idx, hmm_to_n_id
                    to_n_existed = connect_exploded_nodes(
                        exploded,
                        exploded_from_n_id,
                        exploded_to_n_id,
                        None
                    )
                    if not to_n_existed:
                        exploded_from_n_ids.add(exploded_to_n_id)
                    exploded_to_n_ids_non_emitting.add(exploded_to_n_id)
        exploded_from_n_ids = exploded_to_n_ids_emitting
        exploded_from_n_emissions_idx += 1
        exploded_to_n_emissions_idx += 1
    # Ensure all emitted symbols were consumed when exploding out to exploded.
    assert exploded_to_n_emissions_idx == len(emissions)
    # Explode out the non-emitting hidden states of the final last emission index (does not happen in the above loop).
    exploded_to_n_ids_non_emitting = set()
    exploded_from_n_ids = exploded_to_n_ids_emitting.copy()
    while exploded_from_n_ids:
        exploded_from_n_id = exploded_from_n_ids.pop()
        _, hmm_from_n_id = exploded_from_n_id
        for _, _, hmm_to_n_id, _ in hmm.get_outputs_full(hmm_from_n_id):
            hmm_to_n_emittable = hmm.get_node_data(hmm_to_n_id).is_emittable()
            if hmm_to_n_emittable:
                continue
            exploded_to_n_id = exploded_from_n_emissions_idx, hmm_to_n_id
            connect_exploded_nodes(
                exploded,
                exploded_from_n_id,
                exploded_to_n_id,
                None
            )
            exploded_to_n_ids_non_emitting.add(exploded_to_n_id)
            exploded_from_n_ids.add(exploded_to_n_id)
    # Add exploded sink node.
    exploded_to_n_id = -1, hmm_sink_n_id
    for exploded_from_n_id in exploded_to_n_ids_emitting | exploded_to_n_ids_non_emitting:
        connect_exploded_nodes(exploded, exploded_from_n_id, exploded_to_n_id, None)
    return exploded


def connect_exploded_nodes(
        exploded: Graph[EXPLODED_NODE_ID, Any, EXPLODED_EDGE_ID, float],
        exploded_from_n_id: EXPLODED_NODE_ID,
        exploded_to_n_id: EXPLODED_NODE_ID,
        weight: Any
) -> bool:
    to_n_existed = True
    if not exploded.has_node(exploded_to_n_id):
        exploded.insert_node(exploded_to_n_id)
        to_n_existed = False
    exploded_e_weight = weight
    exploded_e_id = exploded_from_n_id, exploded_to_n_id
    exploded.insert_edge(
        exploded_e_id,
        exploded_from_n_id,
        exploded_to_n_id,
        exploded_e_weight
    )
    return to_n_existed


def exploded_to_dot(g: Graph[EXPLODED_NODE_ID, Any, EXPLODED_EDGE_ID, Any]) -> str:
    ret = 'digraph G {\n'
    ret += ' graph[rankdir=LR]\n'
    ret += ' node[shape=egg, fontname="Courier-Bold", fontsize=10]\n'
    ret += ' edge[fontname="Courier-Bold", fontsize=10]\n'
    for n in sorted(g.get_nodes()):
        data = g.get_node_data(n)
        if data is None:
            ret += f'"{n}" [label="{n}"]\n'
        else:
            ret += f'"{n}" [label="{n}\\n{data}"]\n'
    for e in sorted(g.get_edges()):
        n1, n2, data = g.get_edge(e)
        if data is None:
            ret += f'"{n1}" -> "{n2}"\n'
        else:
            ret += f'"{n1}" -> "{n2}" [label="{data}"]\n'
    ret += '}'
    return ret


# MARKDOWN
def emission_probability(
        hmm: Graph[STATE, HmmNodeData, TRANSITION, HmmEdgeData],
        hmm_source_n_id: STATE,
        hmm_sink_n_id: STATE,
        emitted_seq: list[SYMBOL],
        emitted_seq_idx_of_interest: int,
        hidden_state_of_interest: STATE
):
    # Compute forward exploded HMM
    forward_exploded = explode_hmm(hmm, hmm_source_n_id, hmm_sink_n_id, emitted_seq)
    f_sink = forward_exploded_hmm_calculation(hmm, forward_exploded, emitted_seq)
    # Compute backward exploded HMM
    backward_exploded, _ = backward_exploded_hmm_calculation(hmm, hmm_source_n_id, hmm_sink_n_id, emitted_seq)
    # Return
    forward_exploded_n_id = emitted_seq_idx_of_interest, hidden_state_of_interest
    backward_exploded_n_id = emitted_seq_idx_of_interest, hidden_state_of_interest
    f = forward_exploded.get_node_data(forward_exploded_n_id)
    b = backward_exploded.get_node_data(backward_exploded_n_id)
    prob = f * b / f_sink
    return forward_exploded, backward_exploded, prob


def forward_exploded_hmm_calculation(
        hmm: Graph[STATE, HmmNodeData, TRANSITION, HmmEdgeData],
        exploded: Graph[EXPLODED_NODE_ID, Any, EXPLODED_EDGE_ID, Any],
        emitted_seq: list[SYMBOL]
) -> float:
    # Use graph algorithm to figure out emission probability
    exploded_source_n_id = exploded.get_root_node()  # equiv to (-1, hmm_source_n_id) -- using root node func for clarity
    exploded_sink_n_id = exploded.get_leaf_node()  # equiv to (-1, hmm_sink_n_id) -- using leaf node func for clarity
    exploded.update_node_data(exploded_source_n_id, 1.0)
    exploded_to_n_ids = set()
    add_ready_to_process_outgoing_nodes(exploded, exploded_source_n_id, exploded_to_n_ids)
    while exploded_to_n_ids:
        exploded_to_n_id = exploded_to_n_ids.pop()
        # Don't process SINK node in this loop because of the emittable check / emission probability extraction: The
        # sink node is not a hidden state in the HMM (it's only a node in the exploded graph) meaning it will fail if
        # you try to query if its emittable / its emission probabilities.
        if exploded_to_n_id == exploded_sink_n_id:
            continue
        exploded_to_n_emissions_idx, hmm_to_n_id = exploded_to_n_id
        # Get the symbol emission probability for some symbol at the current hidden state. If the hidden state is
        # non-emittable, use 1.0 instead.
        symbol = emitted_seq[exploded_to_n_emissions_idx]
        if hmm.get_node_data(hmm_to_n_id).is_emittable():
            symbol_emission_prob = hmm.get_node_data(hmm_to_n_id).get_symbol_emission_probability(symbol)
        else:
            symbol_emission_prob = 1.0
        # Calculate forward weight for current node
        exploded_to_forward_weight = 0.0
        for _, exploded_from_n_id, _, _ in exploded.get_inputs_full(exploded_to_n_id):
            _, hmm_from_n_id = exploded_from_n_id
            exploded_from_forward_weight = exploded.get_node_data(exploded_from_n_id)
            transition = hmm_from_n_id, hmm_to_n_id
            transition_prob = hmm.get_edge_data(transition).get_transition_probability()
            exploded_to_forward_weight += exploded_from_forward_weight * transition_prob * symbol_emission_prob
            # NOTE: The Pevzner book's formulas did it slightly differently. It factors out multiplication of
            # symbol_emission_prob such that it's applied only once after the loop finishes
            # (e.g. a*b*5+c*d*5+e*f*5 = 5*(a*b+c*d+e*f)). I didn't factor out symbol_emission_prob because I wanted the
            # code to line-up with the diagrams I created for the algorithm documentation.
        exploded.update_node_data(exploded_to_n_id, exploded_to_forward_weight)
        # Now that the forward weight's been calculated for this node, check its outgoing neighbours to see if they're
        # also ready and add them to the ready set if they are.
        add_ready_to_process_outgoing_nodes(exploded, exploded_to_n_id, exploded_to_n_ids)
    # The code above doesn't cover the SINK node -- run a cycle for the SINK node as well here.
    exploded_sink_forward_weight = 0.0
    for _, exploded_from_n_id, _, _ in exploded.get_inputs_full(exploded_sink_n_id):
        exploded_from_forward_weight = exploded.get_node_data(exploded_from_n_id)
        transition_prob = 1.0
        exploded_sink_forward_weight += exploded_from_forward_weight * transition_prob
    exploded.update_node_data(exploded_sink_n_id, exploded_sink_forward_weight)
    # SINK node's weight should be the emission probability
    return exploded_sink_forward_weight


# Given a node in the exploded graph (exploded_n_from_id), look at each outgoing neighbours that it has
# (exploded_to_n_id). If that outgoing neighbour (exploded_to_n_id) has a "forward weight" set for all of its incoming
# neighbours, add it to the set of "ready_to_process" nodes.
def add_ready_to_process_outgoing_nodes(
        exploded: Graph[EXPLODED_NODE_ID, Any, EXPLODED_EDGE_ID, Any],
        exploded_n_from_id: EXPLODED_NODE_ID,
        ready_to_process_n_ids: set[EXPLODED_NODE_ID]
):
    for _, _, exploded_to_n_id, _ in exploded.get_outputs_full(exploded_n_from_id):
        ready_to_process = all(exploded.get_node_data(n) is not None for _, n, _, _ in exploded.get_inputs_full(exploded_to_n_id))
        if ready_to_process:
            ready_to_process_n_ids.add(exploded_to_n_id)


def backward_exploded_hmm_calculation(
        hmm: Graph[STATE, HmmNodeData, TRANSITION, HmmEdgeData],
        hmm_source_n_id: STATE,
        hmm_sink_n_id: STATE,
        emitted_seq: list[SYMBOL]
):
    exploded = explode_hmm(hmm, hmm_source_n_id, hmm_sink_n_id, emitted_seq)
    exploded_source_n_id = exploded.get_root_node()  # equiv to (-1, hmm_source_n_id) -- using root node func for clarity
    exploded_sink_n_id = exploded.get_leaf_node()  # equiv to (-1, hmm_sink_n_id) -- using leaf node func for clarity
    exploded.update_node_data(exploded_sink_n_id, 1.0)
    exploded_from_n_ids = set()
    add_ready_to_process_incoming_nodes(exploded, exploded_sink_n_id, exploded_from_n_ids)
    while exploded_from_n_ids:
        exploded_from_n_id = exploded_from_n_ids.pop()
        if exploded_from_n_id == exploded_source_n_id:
            continue
        _, hmm_from_n_id = exploded_from_n_id
        exploded_from_backward_weight = 0.0
        for _, _, exploded_to_n_id, _ in exploded.get_outputs_full(exploded_from_n_id):
            exploded_to_backward_weight = exploded.get_node_data(exploded_to_n_id)
            exploded_to_n_emissions_idx, hmm_to_n_id = exploded_to_n_id
            if hmm_to_n_id == hmm_sink_n_id:
                transition_prob = 1.0
                symbol_emission_prob = 1.0
            else:
                transition = hmm_from_n_id, hmm_to_n_id
                transition_prob = hmm.get_edge_data(transition).get_transition_probability()
                # Get the symbol emission probability for some symbol at the current hidden state. If the hidden state
                # is non-emittable, use 1.0 instead.
                if hmm_to_n_id != hmm_sink_n_id and hmm.get_node_data(hmm_to_n_id).is_emittable():
                    symbol = emitted_seq[exploded_to_n_emissions_idx]
                    symbol_emission_prob = hmm.get_node_data(hmm_to_n_id).get_symbol_emission_probability(symbol)
                else:
                    symbol_emission_prob = 1.0
            exploded_from_backward_weight += exploded_to_backward_weight * transition_prob * symbol_emission_prob
        exploded.update_node_data(exploded_from_n_id, exploded_from_backward_weight)
        add_ready_to_process_incoming_nodes(exploded, exploded_from_n_id, exploded_from_n_ids)
    # The code above doesn't cover the SOURCE node -- run a cycle for the SOURCE node as well here.
    exploded_source_backward_weight = 0.0
    for _, _, exploded_to_n_id, _ in exploded.get_outputs_full(exploded_source_n_id):
        exploded_to_backward_weight = exploded.get_node_data(exploded_to_n_id)
        _, hmm_source_n_id = exploded_source_n_id
        _, hmm_to_n_id = exploded_to_n_id
        transition = hmm_source_n_id, hmm_to_n_id
        transition_prob = hmm.get_edge_data(transition).get_transition_probability()
        exploded_source_backward_weight += exploded_to_backward_weight * transition_prob
    exploded.update_node_data(exploded_source_n_id, exploded_source_backward_weight)
    # SOURCE node's weight should be the emission probability
    return exploded, exploded_source_backward_weight


# Given a node in the exploded graph (exploded_n_from_id), look at each outgoing neighbours that it has
# (exploded_to_n_id). If that outgoing neighbour (exploded_to_n_id) has a "forward weight" set for all of its incoming
# neighbours, add it to the set of "ready_to_process" nodes.
def add_ready_to_process_incoming_nodes(
        exploded: Graph[EXPLODED_NODE_ID, Any, EXPLODED_EDGE_ID, Any],
        exploded_n_from_id: EXPLODED_NODE_ID,
        ready_to_process_n_ids: set[EXPLODED_NODE_ID]
):
    for _, exploded_from_n_id, _, _ in exploded.get_inputs_full(exploded_n_from_id):
        ready_to_process = all(exploded.get_node_data(n) is not None for _, _, n, _ in exploded.get_outputs_full(exploded_from_n_id))
        if ready_to_process:
            ready_to_process_n_ids.add(exploded_from_n_id)
# MARKDOWN


hmm = to_hmm_graph_PRE_PSEUDOCOUNTS(
    # {
    #     'SOURCE': {'A': 0.5, 'B': 0.5},
    #     'A': {'A': 0.911, 'B': 0.089},
    #     'B': {'A': 0.228, 'B': 0.772},
    # },
    # {
    #     'SOURCE': {},
    #     'A': {'x': 0.356, 'y': 0.191, 'z': 0.453},
    #     'B': {'x': 0.040, 'y': 0.467, 'z': 0.493},
    # }
    {
        'SOURCE': {'A': 0.5, 'B': 0.5},
        'A': {'A': 0.377, 'B': 0.623},
        'B': {'A': 0.301, 'C': 0.699},
        'C': {'B': 1.0}
    },
    {
        'SOURCE': {},
        'A': {'x': 0.176, 'y': 0.596, 'z': 0.228},
        'B': {'x': 0.225, 'y': 0.572, 'z': 0.203},
        'C': {}
    }
)
# emitted_seq = list('zyxxxxyxzz')
emitted_seq = list('zzy')
exploded = explode_hmm(hmm, 'SOURCE', 'SINK', emitted_seq)
_, _, a = emission_probability(hmm, 'SOURCE', 'SINK', emitted_seq, 2, 'A')
_, bg, b = emission_probability(hmm, 'SOURCE', 'SINK', emitted_seq, 2, 'B')
print(f'{exploded_to_dot(bg)}')
print(f'{a=} {b=}')
raise ValueError()
# backward_exploded_hmm_calculation(hmm, exploded, emitted_seq)


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        data_raw = ''.join(stdin.readlines())
        data: dict = yaml.safe_load(data_raw)
        transition_probabilities = data['transition_probabilities']
        emission_probabilities = data['emission_probabilities']
        source_state = data['source_state']
        sink_state = data['sink_state']
        emissions = data['emissions']
        emission_idx_of_interest = data['emission_index_of_interest']
        hidden_state_of_interest = data['hidden_state_of_interest']
        pseudocount = data['pseudocount']
        print(f'Finding the probability of an HMM emitting a sequence, using the following settings...')
        print()
        print('```')
        print(data_raw)
        print('```')
        print()
        hmm = to_hmm_graph_PRE_PSEUDOCOUNTS(transition_probabilities, emission_probabilities)
        hmm_add_pseudocounts_to_hidden_state_transition_probabilities(
            hmm,
            pseudocount
        )
        hmm_add_pseudocounts_to_symbol_emission_probabilities(
            hmm,
            pseudocount
        )
        print(f'The following HMM was produced AFTER applying pseudocounts ...')
        print()
        print('```{dot}')
        print(f'{hmm_to_dot(hmm)}')
        print('```')
        print()
        full_exploded, isolated_exploded, probability = emission_probability(
            hmm,
            source_state,
            sink_state,
            emissions,
            emission_idx_of_interest,
            hidden_state_of_interest
        )
        print(f'The following exploded HMM was produced for the HMM and the emitted sequence {emissions} ...')
        print()
        print('```{dot}')
        print(f'{exploded_to_dot(full_exploded)}')
        print('```')
        print()
        print(f'The exploded HMM was modified such that index {emission_idx_of_interest} only has the option to'
              f' {hidden_state_of_interest} ...')
        print()
        print('```{dot}')
        print(f'{exploded_to_dot(isolated_exploded)}')
        print('```')
        print()
        print(f'The probability of {emissions} being emitted when index {emission_idx_of_interest} only has the option'
              f' to emit from {hidden_state_of_interest} is {probability}.')
        print()
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()
