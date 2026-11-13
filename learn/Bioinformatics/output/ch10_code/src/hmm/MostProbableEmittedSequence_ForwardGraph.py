from collections import defaultdict
from sys import stdin
from typing import Any

import yaml

from graph.DirectedGraph import Graph
from hmm.MostProbableHiddenPath_ViterbiNonEmittingHiddenStates import STATE, SYMBOL, HmmNodeData, TRANSITION, \
    HmmEdgeData, to_hmm_graph_PRE_PSEUDOCOUNTS, hmm_to_dot, \
    hmm_add_pseudocounts_to_hidden_state_transition_probabilities, hmm_add_pseudocounts_to_symbol_emission_probabilities

# MARKDOWN_EXPLODE
LAYERED_FORWARD_EXPLODED_NODE_ID = tuple[int, STATE, SYMBOL | None]
LAYERED_FORWARD_EXPLODED_EDGE_ID = tuple[LAYERED_FORWARD_EXPLODED_NODE_ID, LAYERED_FORWARD_EXPLODED_NODE_ID]


def layer_explode_hmm(
        hmm: Graph[STATE, HmmNodeData, TRANSITION, HmmEdgeData],
        hmm_source_n_id: STATE,
        hmm_sink_n_id: STATE,
        symbols: set[SYMBOL],
        emission_len: int
) -> Graph[LAYERED_FORWARD_EXPLODED_NODE_ID, Any, LAYERED_FORWARD_EXPLODED_EDGE_ID, Any]:
    f_exploded = Graph()
    # Add exploded source node.
    f_exploded_source_n_id = -1, hmm_source_n_id, None
    f_exploded.insert_node(f_exploded_source_n_id)
    # Explode out HMM into new graph.
    f_exploded_from_n_emissions_idx = -1
    f_exploded_from_n_ids = {f_exploded_source_n_id}
    f_exploded_to_n_emissions_idx = 0
    f_exploded_to_n_ids_emitting = set()
    f_exploded_to_n_ids_non_emitting = set()
    while f_exploded_from_n_ids and f_exploded_to_n_emissions_idx < emission_len:
        f_exploded_to_n_ids_emitting = set()
        f_exploded_to_n_ids_non_emitting = set()
        while f_exploded_from_n_ids:
            f_exploded_from_n_id = f_exploded_from_n_ids.pop()
            _, hmm_from_n_id, f_exploded_from_symbol = f_exploded_from_n_id
            for f_exploded_to_n_symbol in symbols:
                for _, _, hmm_to_n_id, _ in hmm.get_outputs_full(hmm_from_n_id):
                    hmm_to_n_emittable = hmm.get_node_data(hmm_to_n_id).is_emittable()
                    if hmm_to_n_emittable:
                        f_exploded_to_n_id = f_exploded_to_n_emissions_idx, hmm_to_n_id, f_exploded_to_n_symbol
                        connect_exploded_nodes(
                            f_exploded,
                            f_exploded_from_n_id,
                            f_exploded_to_n_id,
                            None
                        )
                        f_exploded_to_n_ids_emitting.add(f_exploded_to_n_id)
                    else:
                        f_exploded_to_n_id = f_exploded_from_n_emissions_idx, hmm_to_n_id, f_exploded_to_n_symbol
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
    assert f_exploded_to_n_emissions_idx == emission_len
    # Explode out the non-emitting hidden states of the final last emission index (does not happen in the above loop).
    f_exploded_to_n_ids_non_emitting = set()
    f_exploded_from_n_ids = f_exploded_to_n_ids_emitting.copy()
    while f_exploded_from_n_ids:
        f_exploded_from_n_id = f_exploded_from_n_ids.pop()
        _, hmm_from_n_id, f_exploded_from_symbol = f_exploded_from_n_id
        for f_exploded_to_n_symbol in symbols:
            for _, _, hmm_to_n_id, _ in hmm.get_outputs_full(hmm_from_n_id):
                hmm_to_n_emittable = hmm.get_node_data(hmm_to_n_id).is_emittable()
                if hmm_to_n_emittable:
                    continue
                f_exploded_to_n_id = f_exploded_from_n_emissions_idx, hmm_to_n_id, f_exploded_to_n_symbol
                connect_exploded_nodes(
                    f_exploded,
                    f_exploded_from_n_id,
                    f_exploded_to_n_id,
                    None
                )
                f_exploded_to_n_ids_non_emitting.add(f_exploded_to_n_id)
                f_exploded_from_n_ids.add(f_exploded_to_n_id)
    # Add exploded sink node.
    f_exploded_to_n_id = -1, hmm_sink_n_id, None
    for f_exploded_from_n_id in f_exploded_to_n_ids_emitting | f_exploded_to_n_ids_non_emitting:
        connect_exploded_nodes(f_exploded, f_exploded_from_n_id, f_exploded_to_n_id, None)
    return f_exploded


def connect_exploded_nodes(
        f_exploded: Graph[LAYERED_FORWARD_EXPLODED_NODE_ID, Any, LAYERED_FORWARD_EXPLODED_EDGE_ID, float],
        f_exploded_from_n_id: LAYERED_FORWARD_EXPLODED_NODE_ID,
        f_exploded_to_n_id: LAYERED_FORWARD_EXPLODED_NODE_ID,
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
# MARKDOWN_EXPLODE


def exploded_to_dot(g: Graph[LAYERED_FORWARD_EXPLODED_NODE_ID, Any, LAYERED_FORWARD_EXPLODED_EDGE_ID, Any]) -> str:
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


def main_explode():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        data_raw = ''.join(stdin.readlines())
        data: dict = yaml.safe_load(data_raw)
        transition_probabilities = data['transition_probabilities']
        emission_probabilities = data['emission_probabilities']
        source_state = data['source_state']
        sink_state = data['sink_state']
        emission_len = data['emission_len']
        pseudocount = data['pseudocount']
        print(f'Building exploded graph after applying psuedocounts to HMM, using the following settings...')
        print()
        print('```')
        print(data_raw)
        print('```')
        print()
        hmm = to_hmm_graph_PRE_PSEUDOCOUNTS(transition_probabilities, emission_probabilities)
        print(f'The following HMM was produced before applying pseudocounts ...')
        print()
        print('```{dot}')
        print(f'{hmm_to_dot(hmm)}')
        print('```')
        print()
        hmm_add_pseudocounts_to_hidden_state_transition_probabilities(
            hmm,
            pseudocount
        )
        hmm_add_pseudocounts_to_symbol_emission_probabilities(
            hmm,
            pseudocount
        )
        print(f'After pseudocounts are applied, the HMM becomes as follows ...')
        print()
        print('```{dot}')
        print(f'{hmm_to_dot(hmm)}')
        print('```')
        print()
        exploded = layer_explode_hmm(
            hmm,
            source_state,
            sink_state,
            set(symbol for values in emission_probabilities.values() for symbol in values),
            emission_len
        )
        print(f'The following exploded graph was produced for the HMM and an emission length of {emission_len} ...')
        print()
        print('```{dot}')
        print(f'{exploded_to_dot(exploded)}')
        print('```')
        print()
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")













# MARKDOWN_CALCULATE
def compute_layer_exploded_max_emission_weights(
        hmm: Graph[STATE, HmmNodeData, TRANSITION, HmmEdgeData],
        f_exploded: Graph[LAYERED_FORWARD_EXPLODED_NODE_ID, Any, LAYERED_FORWARD_EXPLODED_EDGE_ID, float]
) -> float:
    # Use graph algorithm to figure out emission probability
    f_exploded_source_n_id = f_exploded.get_root_node()
    f_exploded_sink_n_id = f_exploded.get_leaf_node()
    f_exploded.update_node_data(f_exploded_source_n_id, (None, 1.0))
    f_exploded_to_n_ids = set()
    add_ready_to_process_outgoing_nodes(f_exploded, f_exploded_source_n_id, f_exploded_to_n_ids)
    while f_exploded_to_n_ids:
        f_exploded_to_n_id = f_exploded_to_n_ids.pop()
        f_exploded_to_n_emissions_idx, hmm_to_n_id, f_exploded_to_symbol = f_exploded_to_n_id
        # Determine symbol emission prob. In certain cases, the SINK node may exist in the HMM. Here we check that the
        # node exists in the HMM and that it's emmitable before getting the emission prob.
        if hmm.has_node(hmm_to_n_id) and hmm.get_node_data(hmm_to_n_id).is_emittable():
            symbol_emission_prob = hmm.get_node_data(hmm_to_n_id).get_symbol_emission_probability(f_exploded_to_symbol)
        else:
            symbol_emission_prob = 1.0  # No emission - setting to 1.0 means it has no effect in multiplication later on
        # Calculate forward weight for current node
        f_exploded_to_forward_weights = defaultdict(lambda: 0.0)
        for _, f_exploded_from_n_id, _, _ in f_exploded.get_inputs_full(f_exploded_to_n_id):
            _, hmm_from_n_id, f_exploded_from_symbol = f_exploded_from_n_id
            _, exploded_from_forward_weight = f_exploded.get_node_data(f_exploded_from_n_id)
            # Determine transition prob. In certain cases, the SINK node may exist in the HMM. Here we check that the
            # transition exists in the HMM. If it does, we use the transition prob.
            transition = hmm_from_n_id, hmm_to_n_id
            if hmm.has_edge(transition):
                transition_prob = hmm.get_edge_data(transition).get_transition_probability()
            else:
                transition_prob = 1.0  # Setting to 1.0 means it always happens
            f_exploded_to_forward_weights[
                f_exploded_from_symbol] += exploded_from_forward_weight * transition_prob * symbol_emission_prob
            # NOTE: The Pevzner book's formulas did it slightly differently. It factors out multiplication of
            # symbol_emission_prob such that it's applied only once after the loop finishes
            # (e.g. a*b*5+c*d*5+e*f*5 = 5*(a*b+c*d+e*f)). I didn't factor out symbol_emission_prob because I wanted the
            # code to line-up with the diagrams I created for the algorithm documentation.
        max_layer_symbol, max_value_value = max(f_exploded_to_forward_weights.items(), key=lambda item: item[1])
        f_exploded.update_node_data(f_exploded_to_n_id, (max_layer_symbol, max_value_value))
        # Now that the forward weight's been calculated for this node, check its outgoing neighbours to see if they're
        # also ready and add them to the ready set if they are.
        add_ready_to_process_outgoing_nodes(f_exploded, f_exploded_to_n_id, f_exploded_to_n_ids)
    # SINK node's weight should be the emission probability
    _, f_exploded_sink_forward_weight = f_exploded.get_node_data(f_exploded_sink_n_id)
    return f_exploded_sink_forward_weight


# Given a node in the exploded graph (exploded_n_from_id), look at each outgoing neighbours that it has
# (exploded_to_n_id). If that outgoing neighbour (exploded_to_n_id) has a "forward weight" set for all of its incoming
# neighbours, add it to the set of "ready_to_process" nodes.
def add_ready_to_process_outgoing_nodes(
        f_exploded: Graph[LAYERED_FORWARD_EXPLODED_NODE_ID, Any, LAYERED_FORWARD_EXPLODED_EDGE_ID, float],
        f_exploded_n_from_id: LAYERED_FORWARD_EXPLODED_NODE_ID,
        ready_to_process_n_ids: set[LAYERED_FORWARD_EXPLODED_NODE_ID]
):
    for _, _, f_exploded_to_n_id, _ in f_exploded.get_outputs_full(f_exploded_n_from_id):
        ready_to_process = True
        for _, n, _, _ in f_exploded.get_inputs_full(f_exploded_to_n_id):
            if f_exploded.get_node_data(n) is None:
                ready_to_process = False
        if ready_to_process:
            ready_to_process_n_ids.add(f_exploded_to_n_id)
# MARKDOWN_CALCULATE


def main_calculate():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        data_raw = ''.join(stdin.readlines())
        data: dict = yaml.safe_load(data_raw)
        transition_probabilities = data['transition_probabilities']
        emission_probabilities = data['emission_probabilities']
        source_state = data['source_state']
        sink_state = data['sink_state']
        emission_len = data['emission_len']
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
        print()
        exploded = layer_explode_hmm(
            hmm,
            source_state,
            sink_state,
            set(symbol for values in emission_probabilities.values() for symbol in values),
            emission_len
        )
        print(f'The following exploded graph was produced for the HMM and an emission length of {emission_len} ...')
        print()
        print('```{dot}')
        print(f'{exploded_to_dot(exploded)}')
        print('```')
        print()
        probability = compute_layer_exploded_max_emission_weights(
            hmm,
            exploded
        )
        print(f'The following exploded graph forward and layer backtracking pointers were produced for the exploded graph...')
        print()
        print('```{dot}')
        print(f'{exploded_to_dot(exploded)}')
        print('```')
        print()
        print(f'Between all emissions of length {emission_len}, the emitted sequence with the max probability is {probability} ...')
        print()
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")











# MARKDOWN_BACKTRACK
def backtrack(
        hmm: Graph[STATE, HmmNodeData, TRANSITION, HmmEdgeData],
        exploded: Graph[LAYERED_FORWARD_EXPLODED_NODE_ID, Any, LAYERED_FORWARD_EXPLODED_EDGE_ID, float]
) -> list[SYMBOL]:
    exploded_source_n_id = exploded.get_root_node()
    exploded_sink_n_id = exploded.get_leaf_node()
    _, hmm_sink_n_id, _ = exploded_sink_n_id
    exploded_to_n_id = exploded_sink_n_id
    exploded_last_emission_idx, _, _ = exploded_to_n_id
    emitted_seq = []
    while exploded_to_n_id != exploded_source_n_id:
        _, hmm_to_n_id, exploded_to_layer = exploded_to_n_id
        # Add exploded_to_n_id's layer to the emitted sequence if it's an emittable node. The layer is represented by
        # the symbol for that layer, so the symbol is being added to the emitted sequence. The SINK node may not exist
        # in the HMM, so if exploded_to_n_id is the SINK node, filter it out of test (SINK node will never emit a symbol
        # and isn't part of a layer).
        if hmm_to_n_id != hmm_sink_n_id and hmm.get_node_data(hmm_to_n_id).is_emittable():
            emitted_seq.insert(0, exploded_to_layer)
        backtracking_layer, _ = exploded.get_node_data(exploded_to_n_id)
        # The backtracking symbol is the layer this came from. Collect all nodes in that layer that have edges to
        # exploded_to_n_id.
        exploded_from_n_id_and_weights = []
        for _, exploded_from_n_id, _, _ in exploded.get_inputs_full(exploded_to_n_id):
            _, _, exploded_from_layer = exploded_from_n_id
            if exploded_from_layer != backtracking_layer:
                continue
            _, weight = exploded.get_node_data(exploded_from_n_id)
            exploded_from_n_id_and_weights.append((weight, exploded_from_n_id))
        # Of those collected nodes, the one with the maximum weight is the one that gets selected.
        _, exploded_to_n_id = max(exploded_from_n_id_and_weights, key=lambda x: x[0])
    return emitted_seq
# MARKDOWN_BACKTRACK


def main_backtrack():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        data_raw = ''.join(stdin.readlines())
        data: dict = yaml.safe_load(data_raw)
        transition_probabilities = data['transition_probabilities']
        emission_probabilities = data['emission_probabilities']
        source_state = data['source_state']
        sink_state = data['sink_state']
        emission_len = data['emission_len']
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
        exploded = layer_explode_hmm(
            hmm,
            source_state,
            sink_state,
            set(symbol for values in emission_probabilities.values() for symbol in values),
            emission_len
        )
        print(f'The following exploded graph was produced for the HMM and an emission length of {emission_len} ...')
        print()
        print('```{dot}')
        print(f'{exploded_to_dot(exploded)}')
        print('```')
        print()
        probability = compute_layer_exploded_max_emission_weights(
            hmm,
            exploded
        )
        print(f'The following exploded graph forward and layer backtracking pointers were produced for the exploded graph...')
        print()
        print('```{dot}')
        print(f'{exploded_to_dot(exploded)}')
        print('```')
        print()
        emitted_seq = backtrack(
            hmm,
            exploded
        )
        print(f'The sequence {emitted_seq} is the most probable for any emitted sequence of length {emission_len} ({probability=}) ...')
        print()
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")










# transition_probs = {
#     'SOURCE': {'A': 0.5, 'B': 0.5},
#     'A': {'A': 0.377, 'B': 0.623},
#     'B': {'A': 0.301, 'C': 0.699},
#     'C': {"B": 1.0}
# }
# emission_probs = {
#     'SOURCE': {},
#     'A': {'y': 0.596, 'z': 0.404},
#     'B': {'y': 0.572, 'z': 0.428},
#     'C': {}
# }
# hmm = to_hmm_graph_PRE_PSEUDOCOUNTS(transition_probs, emission_probs)
# exploded = explode_hmm(
#     hmm,
#     'SOURCE',
#     'SINK',
#     {'y', 'z'},
#     3,
#     lambda g, st: emission_probs[st] != {}
# )
# compute_exploded_max_emission_weights(
#     hmm,
#     exploded,
#     lambda g, st, sy: emission_probs[st][sy],
#     lambda g, st: emission_probs[st] != {},
#     lambda g, st1, st2: transition_probs[st1][st2]
# )
# emitted_seq = backtrack(
#     hmm,
#     exploded,
#     lambda g, st: emission_probs[st] != {}
# )
# print(f'{emitted_seq=}')


if __name__ == '__main__':
    main_backtrack()
