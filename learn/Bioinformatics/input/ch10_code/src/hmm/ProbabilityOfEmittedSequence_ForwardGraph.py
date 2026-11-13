from sys import stdin
from typing import Any, Literal

import yaml

from graph.DirectedGraph import Graph
from hmm.MostProbableHiddenPath_ViterbiNonEmittingHiddenStates import STATE, HmmNodeData, TRANSITION, HmmEdgeData, \
    SYMBOL, to_hmm_graph_PRE_PSEUDOCOUNTS, hmm_add_pseudocounts_to_hidden_state_transition_probabilities, \
    hmm_add_pseudocounts_to_symbol_emission_probabilities, hmm_to_dot

FORWARD_EXPLODED_NODE_ID = tuple[int, STATE]
FORWARD_EXPLODED_EDGE_ID = tuple[FORWARD_EXPLODED_NODE_ID, FORWARD_EXPLODED_NODE_ID]


def forward_explode_hmm(
        hmm: Graph[STATE, HmmNodeData, TRANSITION, HmmEdgeData],
        hmm_source_n_id: STATE,
        hmm_sink_n_id: STATE,
        emissions: list[SYMBOL]
) -> Graph[FORWARD_EXPLODED_NODE_ID, Any, FORWARD_EXPLODED_EDGE_ID, Any]:
    f_exploded = Graph()
    # Add exploded source node.
    f_exploded_source_n_id = -1, hmm_source_n_id
    f_exploded.insert_node(f_exploded_source_n_id)
    # Explode out HMM into new graph.
    f_exploded_from_n_emissions_idx = -1
    f_exploded_from_n_ids = {f_exploded_source_n_id}
    f_exploded_to_n_emissions_idx = 0
    f_exploded_to_n_ids_emitting = set()
    f_exploded_to_n_ids_non_emitting = set()
    while f_exploded_from_n_ids and f_exploded_to_n_emissions_idx < len(emissions):
        f_exploded_to_n_symbol = emissions[f_exploded_to_n_emissions_idx]
        f_exploded_to_n_ids_emitting = set()
        f_exploded_to_n_ids_non_emitting = set()
        while f_exploded_from_n_ids:
            f_exploded_from_n_id = f_exploded_from_n_ids.pop()
            _, hmm_from_n_id = f_exploded_from_n_id
            for _, _, hmm_to_n_id, _ in hmm.get_outputs_full(hmm_from_n_id):
                hmm_to_n_emittable = hmm.get_node_data(hmm_to_n_id).is_emittable()
                if hmm_to_n_emittable:
                    f_exploded_to_n_id = f_exploded_to_n_emissions_idx, hmm_to_n_id
                    connect_exploded_nodes(
                        f_exploded,
                        f_exploded_from_n_id,
                        f_exploded_to_n_id,
                        None
                    )
                    f_exploded_to_n_ids_emitting.add(f_exploded_to_n_id)
                else:
                    f_exploded_to_n_id = f_exploded_from_n_emissions_idx, hmm_to_n_id
                    to_n_existed = connect_exploded_nodes(
                        f_exploded,
                        f_exploded_from_n_id,
                        f_exploded_to_n_id,
                        None
                    )
                    if not to_n_existed:
                        f_exploded_from_n_ids.add(f_exploded_to_n_id)
                    f_exploded_to_n_ids_non_emitting.add(f_exploded_to_n_id)
        f_exploded_from_n_ids = f_exploded_to_n_ids_emitting
        f_exploded_from_n_emissions_idx += 1
        f_exploded_to_n_emissions_idx += 1
    # Ensure all emitted symbols were consumed when exploding out to exploded.
    assert f_exploded_to_n_emissions_idx == len(emissions)
    # Explode out the non-emitting hidden states of the final last emission index (does not happen in the above loop).
    f_exploded_to_n_ids_non_emitting = set()
    f_exploded_from_n_ids = f_exploded_to_n_ids_emitting.copy()
    while f_exploded_from_n_ids:
        f_exploded_from_n_id = f_exploded_from_n_ids.pop()
        _, hmm_from_n_id = f_exploded_from_n_id
        for _, _, hmm_to_n_id, _ in hmm.get_outputs_full(hmm_from_n_id):
            hmm_to_n_emittable = hmm.get_node_data(hmm_to_n_id).is_emittable()
            if hmm_to_n_emittable:
                continue
            f_exploded_to_n_id = f_exploded_from_n_emissions_idx, hmm_to_n_id
            connect_exploded_nodes(
                f_exploded,
                f_exploded_from_n_id,
                f_exploded_to_n_id,
                None
            )
            f_exploded_to_n_ids_non_emitting.add(f_exploded_to_n_id)
            f_exploded_from_n_ids.add(f_exploded_to_n_id)
    # Add exploded sink node.
    f_exploded_to_n_id = -1, hmm_sink_n_id
    for f_exploded_from_n_id in f_exploded_to_n_ids_emitting | f_exploded_to_n_ids_non_emitting:
        connect_exploded_nodes(f_exploded, f_exploded_from_n_id, f_exploded_to_n_id, None)
    return f_exploded


def connect_exploded_nodes(
        f_exploded: Graph[FORWARD_EXPLODED_NODE_ID, Any, FORWARD_EXPLODED_EDGE_ID, float],
        f_exploded_from_n_id: FORWARD_EXPLODED_NODE_ID,
        f_exploded_to_n_id: FORWARD_EXPLODED_NODE_ID,
        weight: Any
) -> bool:
    to_n_existed = True
    if not f_exploded.has_node(f_exploded_to_n_id):
        f_exploded.insert_node(f_exploded_to_n_id)
        to_n_existed = False
    f_exploded_e_weight = weight
    f_exploded_e_id = f_exploded_from_n_id, f_exploded_to_n_id
    f_exploded.insert_edge(
        f_exploded_e_id,
        f_exploded_from_n_id,
        f_exploded_to_n_id,
        f_exploded_e_weight
    )
    return to_n_existed


def exploded_to_dot(
        g: Graph,
        label: str | None = None,
        label_loc: Literal['top', 'bottom'] | None = None,
        rank_dir: Literal['LR', 'RL', 'TB', 'BT'] | None = 'LR'
) -> str:
    ret = 'digraph G {\n'
    if rank_dir is not None:
        ret += f' graph[rankdir={rank_dir}]\n'
    ret += ' node[shape=egg, fontname="Courier-Bold", fontsize=10]\n'
    ret += ' edge[fontname="Courier-Bold", fontsize=10]\n'
    if label is not None:
        ret += f' label="{label}"\n'
    if label_loc is not None:
        ret += f' labelloc={label_loc}\n'
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
        emitted_seq: list[SYMBOL]
) -> tuple[
    Graph[FORWARD_EXPLODED_NODE_ID, Any, FORWARD_EXPLODED_EDGE_ID, Any],
    float
]:
    f_exploded = forward_explode_hmm(hmm, hmm_source_n_id, hmm_sink_n_id, emitted_seq)
    f_exploded_sink_weight = forward_exploded_hmm_calculation(hmm, f_exploded, emitted_seq)
    return f_exploded, f_exploded_sink_weight


def forward_exploded_hmm_calculation(
        hmm: Graph[STATE, HmmNodeData, TRANSITION, HmmEdgeData],
        f_exploded: Graph[FORWARD_EXPLODED_NODE_ID, Any, FORWARD_EXPLODED_EDGE_ID, Any],
        emitted_seq: list[SYMBOL]
) -> float:
    f_exploded_source_n_id = f_exploded.get_root_node()
    f_exploded_sink_n_id = f_exploded.get_leaf_node()
    f_exploded.update_node_data(f_exploded_source_n_id, 1.0)
    f_exploded_to_n_ids = set()
    add_ready_to_process_outgoing_nodes(f_exploded, f_exploded_source_n_id, f_exploded_to_n_ids)
    while f_exploded_to_n_ids:
        f_exploded_to_n_id = f_exploded_to_n_ids.pop()
        f_exploded_to_n_emissions_idx, hmm_to_n_id = f_exploded_to_n_id
        # Determine symbol emission prob. In certain cases, the SINK node may exist in the HMM. Here we check that the
        # node exists in the HMM and that it's emmitable before getting the emission prob.
        symbol = emitted_seq[f_exploded_to_n_emissions_idx]
        if hmm.has_node(hmm_to_n_id) and hmm.get_node_data(hmm_to_n_id).is_emittable():
            symbol_emission_prob = hmm.get_node_data(hmm_to_n_id).get_symbol_emission_probability(symbol)
        else:
            symbol_emission_prob = 1.0  # No emission - setting to 1.0 means it has no effect in multiplication later on
        # Calculate forward weight for current node
        f_exploded_to_forward_weight = 0.0
        for _, exploded_from_n_id, _, _ in f_exploded.get_inputs_full(f_exploded_to_n_id):
            _, hmm_from_n_id = exploded_from_n_id
            f_exploded_from_forward_weight = f_exploded.get_node_data(exploded_from_n_id)
            # Determine transition prob. In certain cases, the SINK node may exist in the HMM. Here we check that the
            # transition exists in the HMM. If it does, we use the transition prob.
            transition = hmm_from_n_id, hmm_to_n_id
            if hmm.has_edge(transition):
                transition_prob = hmm.get_edge_data(transition).get_transition_probability()
            else:
                transition_prob = 1.0  # Setting to 1.0 means it always happens
            f_exploded_to_forward_weight += f_exploded_from_forward_weight * transition_prob * symbol_emission_prob
            # NOTE: The Pevzner book's formulas did it slightly differently. It factors out multiplication of
            # symbol_emission_prob such that it's applied only once after the loop finishes
            # (e.g. a*b*5+c*d*5+e*f*5 = 5*(a*b+c*d+e*f)). I didn't factor out symbol_emission_prob because I wanted the
            # code to line-up with the diagrams I created for the algorithm documentation.
        f_exploded.update_node_data(f_exploded_to_n_id, f_exploded_to_forward_weight)
        # Now that the forward weight's been calculated for this node, check its outgoing neighbours to see if they're
        # also ready and add them to the ready set if they are.
        add_ready_to_process_outgoing_nodes(f_exploded, f_exploded_to_n_id, f_exploded_to_n_ids)
    f_exploded_sink_forward_weight = f_exploded.get_node_data(f_exploded_sink_n_id)
    # SINK node's weight should be the emission probability
    return f_exploded_sink_forward_weight


# Given a node in the exploded graph (f_exploded_n_from_id), look at each outgoing neighbours that it has
# (f_exploded_to_n_id). If that outgoing neighbour (f_exploded_to_n_id) has a "forward weight" set for all of its
# incoming neighbours, add it to the set of "ready_to_process" nodes.
def add_ready_to_process_outgoing_nodes(
        f_exploded: Graph[FORWARD_EXPLODED_NODE_ID, Any, FORWARD_EXPLODED_EDGE_ID, Any],
        f_exploded_n_from_id: FORWARD_EXPLODED_NODE_ID,
        ready_to_process_n_ids: set[FORWARD_EXPLODED_NODE_ID]
):
    for _, _, f_exploded_to_n_id, _ in f_exploded.get_outputs_full(f_exploded_n_from_id):
        ready_to_process = True
        for _, n, _, _ in f_exploded.get_inputs_full(f_exploded_to_n_id):
            if f_exploded.get_node_data(n) is None:
                ready_to_process = False
        if ready_to_process:
            ready_to_process_n_ids.add(f_exploded_to_n_id)
# MARKDOWN


# transition_probs = {
#     'SOURCE': {'A': 0.5, 'B': 0.5},
#     'A': {'A': 0.303, 'B': 0.697},
#     'B': {'A': 0.831, 'B': 0.169},
# }
# emission_probs = {
#     'A': {'x': 0.533, 'y': 0.065, 'z': 0.402},
#     'B': {'x': 0.342, 'y': 0.334, 'z': 0.324}
# }
# prob = emission_probability(
#     to_hmm_graph_PRE_PSEUDOCOUNTS(transition_probs, emission_probs),
#     'SOURCE',
#     'SINK',
#     list('xzyyzzyzyy'),
#     lambda g, st, sy: emission_probs[st][sy],
#     lambda g, st: emission_probs[st] != {},
#     lambda g, st1, st2: transition_probs[st1][st2]
# )
# print(f'{prob}')


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
        f_exploded, probability = emission_probability(
            hmm,
            source_state,
            sink_state,
            emissions
        )
        print(f'The following exploded HMM was produced for the HMM and the emitted sequence {emissions} ...')
        print()
        print('```{dot}')
        print(f'{exploded_to_dot(f_exploded)}')
        print('```')
        print()
        print(f'The probability of {emissions} being emitted is {probability} ...')
        print()
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()
