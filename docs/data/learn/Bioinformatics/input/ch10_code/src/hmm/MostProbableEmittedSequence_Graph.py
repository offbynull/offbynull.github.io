from collections import defaultdict
from sys import stdin
from typing import TypeVar, Callable, Any, Iterable

import yaml

from graph.DirectedGraph import Graph

N = TypeVar('N')
ND = TypeVar('ND')
E = TypeVar('E')
ED = TypeVar('ED')
STATE = TypeVar('STATE')
SYMBOL = TypeVar('SYMBOL')


def exploded_to_dot(g: Graph) -> str:
    ret = 'digraph G {\n'
    ret += ' graph[rankdir=LR]\n'
    ret += ' node[shape=egg, fontname="Courier-Bold", fontsize=10]\n'
    ret += ' edge[fontname="Courier-Bold", fontsize=10]\n'
    for n in sorted(g.get_nodes()):
        weight = g.get_node_data(n)
        if weight is None:
            ret += f'"{n}" [label="{n}"]\n'
        else:
            ret += f'"{n}" [label="{n}\\n{weight}"]\n'
    for e in sorted(g.get_edges()):
        n1, n2, weight = g.get_edge(e)
        if weight is None:
            ret += f'"{n1}" -> "{n2}"\n'
        else:
            ret += f'"{n1}" -> "{n2} [label="{weight}"]\n'
    ret += '}'
    return ret


# MARKDOWN_EXPLODE
def explode_hmm(
        hmm: Graph[N, ND, E, ED],
        hmm_source_n_id: N,
        hmm_sink_n_id: N,
        symbols: set[SYMBOL],
        emission_len: int,
        get_node_emittable: Callable[[Graph[N, ND, E, ED], STATE], bool],
) -> Graph[tuple[int, N, SYMBOL], Any, tuple[N, N], Any]:
    exploded = Graph()
    # Add exploded source node.
    exploded_source_n_id = -1, hmm_source_n_id, None
    exploded.insert_node(exploded_source_n_id)
    # Explode out HMM into new graph.
    exploded_from_n_emissions_idx = -1
    exploded_from_n_ids = {exploded_source_n_id}
    exploded_to_n_emissions_idx = 0
    exploded_to_n_ids_emitting = set()
    exploded_to_n_ids_non_emitting = set()
    while exploded_from_n_ids and exploded_to_n_emissions_idx < emission_len:
        exploded_to_n_ids_emitting = set()
        exploded_to_n_ids_non_emitting = set()
        while exploded_from_n_ids:
            exploded_from_n_id = exploded_from_n_ids.pop()
            _, hmm_from_n_id, exploded_from_symbol = exploded_from_n_id
            for exploded_to_n_symbol in symbols:
                for _, _, hmm_to_n_id, _ in hmm.get_outputs_full(hmm_from_n_id):
                    hmm_to_n_emittable = get_node_emittable(hmm, hmm_to_n_id)
                    if hmm_to_n_emittable:
                        exploded_to_n_id = exploded_to_n_emissions_idx, hmm_to_n_id, exploded_to_n_symbol
                        connect_exploded_nodes(
                            exploded,
                            exploded_from_n_id,
                            exploded_to_n_id,
                            None
                        )
                        exploded_to_n_ids_emitting.add(exploded_to_n_id)
                    else:
                        exploded_to_n_id = exploded_from_n_emissions_idx, hmm_to_n_id, exploded_to_n_symbol
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
    assert exploded_to_n_emissions_idx == emission_len
    # Explode out the non-emitting hidden states of the final last emission index (does not happen in the above loop).
    exploded_to_n_ids_non_emitting = set()
    exploded_from_n_ids = exploded_to_n_ids_emitting.copy()
    while exploded_from_n_ids:
        exploded_from_n_id = exploded_from_n_ids.pop()
        _, hmm_from_n_id, exploded_from_symbol = exploded_from_n_id
        for exploded_to_n_symbol in symbols:
            for _, _, hmm_to_n_id, _ in hmm.get_outputs_full(hmm_from_n_id):
                hmm_to_n_emmitable = get_node_emittable(hmm, hmm_to_n_id)
                if hmm_to_n_emmitable:
                    continue
                exploded_to_n_id = exploded_from_n_emissions_idx, hmm_to_n_id, exploded_to_n_symbol
                connect_exploded_nodes(
                    exploded,
                    exploded_from_n_id,
                    exploded_to_n_id,
                    None
                )
                exploded_to_n_ids_non_emitting.add(exploded_to_n_id)
                exploded_from_n_ids.add(exploded_to_n_id)
    # Add exploded sink node.
    exploded_to_n_id = -1, hmm_sink_n_id, None
    for exploded_from_n_id in exploded_to_n_ids_emitting | exploded_to_n_ids_non_emitting:
        connect_exploded_nodes(exploded, exploded_from_n_id, exploded_to_n_id, None)
    return exploded


def connect_exploded_nodes(
        exploded: Graph[tuple[int, N], Any, tuple[N, N], Any],
        exploded_from_n_id: tuple[int, N, SYMBOL],
        exploded_to_n_id: tuple[int, N, SYMBOL],
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
# MARKDOWN_EXPLODE


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
            pseudocount,
            lambda g: list(g.get_nodes()),
            lambda g, s1: [s2 for _, _, s2, _ in g.get_outputs_full(s1)],
            lambda g, s1, s2: g.get_edge_data((s1, s2)),
            lambda g, s1, s2, weight: g.update_edge_data((s1, s2), weight)
        )
        hmm_add_pseudocounts_to_symbol_emission_probabilities(
            hmm,
            pseudocount,
            lambda g: list(g.get_nodes()),
            lambda g, s1: list(g.get_node_data(s1)),
            lambda g, s1, sym: g.get_node_data(s1)[sym],
            lambda g, s1, sym, weight: g.get_node_data(s1).update({sym: weight})
        )
        print(f'After pseudocounts are applied, the HMM becomes as follows ...')
        print()
        print('```{dot}')
        print(f'{hmm_to_dot(hmm)}')
        print('```')
        print()
        exploded = explode_hmm(
            hmm,
            source_state,
            sink_state,
            set(symbol for values in emission_probabilities.values() for symbol in values),
            emission_len,
            lambda g, state: g.get_node_data(state) != {}
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










def hmm_to_dot(g: Graph) -> str:
    ret = 'digraph G {\n'
    ret += ' graph[rankdir=LR]\n'
    ret += ' node[shape=egg, fontname="Courier-Bold", fontsize=10]\n'
    ret += ' edge[fontname="Courier-Bold", fontsize=10]\n'
    for n in sorted(g.get_nodes()):
        ret += f'"STATE_{n}" [label="{n}"]\n'
    for e in sorted(g.get_edges()):
        n1, n2, weight = g.get_edge(e)
        ret += f'"STATE_{n1}" -> "STATE_{n2}" [label="{weight}"]\n'
    added_symbols = set()
    for n in sorted(g.get_nodes()):
        emission_probs = g.get_node_data(n)
        for n_symbol, weight in emission_probs.items():
            if n_symbol not in added_symbols:
                ret += f'"SYMBOL_{n_symbol}" [label="{n_symbol}", style="dashed"]\n'
                added_symbols.add(n_symbol)
            ret += f'"STATE_{n}" -> "SYMBOL_{n_symbol}" [label="{weight}", style="dashed"]\n'
    ret += '}'
    return ret


def to_hmm_graph_PRE_PSEUDOCOUNTS(
        transition_probabilities: dict[str, dict[str, float]],
        emission_probabilities: dict[str, dict[str, float]]
) -> Graph[str, dict[str, float], tuple[str, str], float]:
    # Does not check that all outgoing transitions sum to 1.0 / all emissions sum to 1.0. These checks need to be done
    # after pseudocounts are applied
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
                weight
            )
    for state in emission_probabilities:
        weights = emission_probabilities[state]
        if not hmm.has_node(state):
            hmm.insert_node(state)
        hmm.update_node_data(state, weights)
    return hmm


def hmm_add_pseudocounts_to_hidden_state_transition_probabilities(
        hmm: Graph[N, ND, E, ED],
        psuedocount: float,
        list_states: [[Graph[N, ND, E, ED]], Iterable[STATE]],
        list_outgoing_state_transitions: [[Graph[N, ND, E, ED], STATE], Iterable[STATE]],
        get_edge_transition_prob: Callable[[Graph[N, ND, E, ED], STATE, STATE], float],
        set_edge_transition_prob: Callable[[Graph[N, ND, E, ED], STATE, STATE, float], None]
) -> None:
    for from_state in list_states(hmm):
        tweaked_transition_weights = {}
        total_transition_weights = 0.0
        for to_state in list_outgoing_state_transitions(hmm, from_state):
            weight = get_edge_transition_prob(hmm, from_state, to_state) + psuedocount
            tweaked_transition_weights[to_state] = weight
            total_transition_weights += weight
        for to_state, weight in tweaked_transition_weights.items():
            normalized_transition_weight = weight / total_transition_weights
            set_edge_transition_prob(hmm, from_state, to_state, normalized_transition_weight)


def hmm_add_pseudocounts_to_symbol_emission_probabilities(
        hmm: Graph[N, ND, E, ED],
        psuedocount: float,
        list_states: [[Graph[N, ND, E, ED]], Iterable[STATE]],
        list_state_emissions: [[Graph[N, ND, E, ED]], Iterable[SYMBOL]],
        get_node_emission_prob: Callable[[Graph[N, ND, E, ED], STATE, SYMBOL], float],
        set_node_emission_prob: Callable[[Graph[N, ND, E, ED], STATE, SYMBOL, float], None],
) -> None:
    for from_state in list_states(hmm):
        tweaked_emission_weights = {}
        total_emission_weights = 0.0
        for symbol in list_state_emissions(hmm, from_state):
            weight = get_node_emission_prob(hmm, from_state, symbol) + psuedocount
            tweaked_emission_weights[symbol] = weight
            total_emission_weights += weight
        for symbol, weight in tweaked_emission_weights.items():
            normalized_transition_weight = weight / total_emission_weights
            set_node_emission_prob(hmm, from_state, symbol, normalized_transition_weight)


# MARKDOWN_CALCULATE
def compute_exploded_max_emission_weights(
        hmm: Graph[N, ND, E, ED],
        exploded: Graph[tuple[int, N, SYMBOL], Any, tuple[N, N], Any],
        get_node_emission_prob: Callable[[Graph[N, ND, E, ED], STATE, SYMBOL], float],
        get_node_emittable: Callable[[Graph[N, ND, E, ED], STATE], bool],
        get_edge_transition_prob: Callable[[Graph[N, ND, E, ED], STATE, STATE], float]
) -> float:
    # Use graph algorithm to figure out emission probability
    exploded_source_n_id = exploded.get_root_node()  # equiv to (-1, hmm_source_n_id) -- using root node func for clarity
    exploded_sink_n_id = exploded.get_leaf_node()  # equiv to (-1, hmm_sink_n_id) -- using leaf node func for clarity
    exploded.update_node_data(exploded_source_n_id, (None, 1.0))
    exploded_to_n_ids = set()
    add_ready_to_process_outgoing_nodes(exploded, exploded_source_n_id, exploded_to_n_ids)
    while exploded_to_n_ids:
        exploded_to_n_id = exploded_to_n_ids.pop()
        # Don't process SINK node in this loop because of the emittable check / emission probability extraction: The
        # sink node is not a hidden state in the HMM (it's only a node in the exploded graph) meaning it will fail if
        # you try to query if its emittable / its emission probabilities.
        if exploded_to_n_id == exploded_sink_n_id:
            continue
        compute_node_forward_weight(hmm, exploded, exploded_to_n_id, get_node_emission_prob, get_node_emittable,
                                    get_edge_transition_prob)
        # Now that the forward weight's been calculated for this node, check its outgoing neighbours to see if they're
        # also ready and add them to the ready set if they are.
        add_ready_to_process_outgoing_nodes(exploded, exploded_to_n_id, exploded_to_n_ids)
    # The code above doesn't cover the SINK node -- run a cycle for the SINK node as well here.
    compute_sink_node_forward_weight(exploded, exploded_sink_n_id)
    # SINK node's weight should be the emission probability
    _, exploded_sink_forward_weight = exploded.get_node_data(exploded_sink_n_id)
    return exploded_sink_forward_weight


def compute_node_forward_weight(
        hmm: Graph[N, ND, E, ED],
        exploded: Graph[tuple[int, N, SYMBOL], Any, tuple[N, N], Any],
        exploded_to_n_id: tuple[int, N, SYMBOL],
        get_node_emission_prob: Callable[[Graph[N, ND, E, ED], STATE, SYMBOL], float],
        get_node_emittable: Callable[[Graph[N, ND, E, ED], STATE], bool],
        get_edge_transition_prob: Callable[[Graph[N, ND, E, ED], STATE, STATE], float]
):
    exploded_to_n_emissions_idx, hmm_to_n_id, exploded_to_symbol = exploded_to_n_id
    # Get the symbol emission probability for some symbol at the current hidden state. If the hidden state is
    # non-emittable, use 1.0 instead.
    if get_node_emittable(hmm, hmm_to_n_id):
        symbol_emission_prob = get_node_emission_prob(hmm, hmm_to_n_id, exploded_to_symbol)
    else:
        symbol_emission_prob = 1.0
    # Calculate forward weight for current node
    exploded_to_forward_weights = defaultdict(lambda: 0.0)
    for _, exploded_from_n_id, _, _ in exploded.get_inputs_full(exploded_to_n_id):
        _, hmm_from_n_id, exploded_from_symbol = exploded_from_n_id
        _, exploded_from_forward_weight = exploded.get_node_data(exploded_from_n_id)
        transition_prob = get_edge_transition_prob(hmm, hmm_from_n_id, hmm_to_n_id)
        exploded_to_forward_weights[exploded_from_symbol] += exploded_from_forward_weight * transition_prob * symbol_emission_prob
        # NOTE: The Pevzner book's formulas did it slightly differently. It factors out multiplication of
        # symbol_emission_prob such that it's applied only once after the loop finishes
        # (e.g. a*b*5+c*d*5+e*f*5 = 5*(a*b+c*d+e*f)). I didn't factor out symbol_emission_prob because I wanted the
        # code to line-up with the diagrams I created for the algorithm documentation.
    max_layer_symbol, max_value_value = max(exploded_to_forward_weights.items(), key=lambda item: item[1])
    exploded.update_node_data(exploded_to_n_id, (max_layer_symbol, max_value_value))


def compute_sink_node_forward_weight(
        exploded: Graph[tuple[int, N, SYMBOL], Any, tuple[N, N], Any],
        exploded_sink_n_id: tuple[int, N, SYMBOL]
):
    transition_prob = 1.0
    # Calculate forward weight for current node
    exploded_to_forward_weights = defaultdict(lambda: 0.0)
    for _, exploded_from_n_id, _, _ in exploded.get_inputs_full(exploded_sink_n_id):
        _, hmm_from_n_id, exploded_from_symbol = exploded_from_n_id
        _, exploded_from_forward_weight = exploded.get_node_data(exploded_from_n_id)
        exploded_to_forward_weights[exploded_from_symbol] += exploded_from_forward_weight * transition_prob
    max_layer_symbol, max_value_value = max(exploded_to_forward_weights.items(), key=lambda item: item[1])
    exploded.update_node_data(exploded_sink_n_id, (max_layer_symbol, max_value_value))


# Given a node in the exploded graph (exploded_n_from_id), look at each outgoing neighbours that it has
# (exploded_to_n_id). If that outgoing neighbour (exploded_to_n_id) has a "forward weight" set for all of its incoming
# neighbours, add it to the set of "ready_to_process" nodes.
def add_ready_to_process_outgoing_nodes(
        exploded: Graph[tuple[int, N, SYMBOL], Any, tuple[N, N], Any],
        exploded_n_from_id: tuple[int, N, SYMBOL],
        ready_to_process_n_ids: set[tuple[int, N, SYMBOL]]
):
    for _, _, exploded_to_n_id, _ in exploded.get_outputs_full(exploded_n_from_id):
        ready_to_process = all(exploded.get_node_data(n) is not None for _, n, _, _ in exploded.get_inputs_full(exploded_to_n_id))
        if ready_to_process:
            ready_to_process_n_ids.add(exploded_to_n_id)
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
            pseudocount,
            lambda g: list(g.get_nodes()),
            lambda g, s1: [s2 for _, _, s2, _ in g.get_outputs_full(s1)],
            lambda g, s1, s2: g.get_edge_data((s1, s2)),
            lambda g, s1, s2, weight: g.update_edge_data((s1, s2), weight)
        )
        hmm_add_pseudocounts_to_symbol_emission_probabilities(
            hmm,
            pseudocount,
            lambda g: list(g.get_nodes()),
            lambda g, s1: list(g.get_node_data(s1)),
            lambda g, s1, sym: g.get_node_data(s1)[sym],
            lambda g, s1, sym, weight: g.get_node_data(s1).update({sym: weight})
        )
        print(f'The following HMM was produced AFTER applying pseudocounts ...')
        print()
        print('```{dot}')
        print(f'{hmm_to_dot(hmm)}')
        print('```')
        print()
        print()
        exploded = explode_hmm(
            hmm,
            source_state,
            sink_state,
            set(symbol for values in emission_probabilities.values() for symbol in values),
            emission_len,
            lambda g, state: g.get_node_data(state) != {}
        )
        print(f'The following exploded graph was produced for the HMM and an emission length of {emission_len} ...')
        print()
        print('```{dot}')
        print(f'{exploded_to_dot(exploded)}')
        print('```')
        print()
        probability = compute_exploded_max_emission_weights(
            hmm,
            exploded,
            lambda g, state, symbol: g.get_node_data(state)[symbol],
            lambda g, state: g.get_node_data(state) != {},
            lambda g, s1, s2: g.get_edge_data((s1, s2))
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
    hmm: Graph[N, ND, E, ED],
    exploded: Graph[tuple[int, N, SYMBOL], Any, tuple[N, N], Any],
    get_node_emittable: Callable[[Graph[N, ND, E, ED], STATE], bool]
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
        if hmm_to_n_id != hmm_sink_n_id and get_node_emittable(hmm, hmm_to_n_id):
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
            pseudocount,
            lambda g: list(g.get_nodes()),
            lambda g, s1: [s2 for _, _, s2, _ in g.get_outputs_full(s1)],
            lambda g, s1, s2: g.get_edge_data((s1, s2)),
            lambda g, s1, s2, weight: g.update_edge_data((s1, s2), weight)
        )
        hmm_add_pseudocounts_to_symbol_emission_probabilities(
            hmm,
            pseudocount,
            lambda g: list(g.get_nodes()),
            lambda g, s1: list(g.get_node_data(s1)),
            lambda g, s1, sym: g.get_node_data(s1)[sym],
            lambda g, s1, sym, weight: g.get_node_data(s1).update({sym: weight})
        )
        print(f'The following HMM was produced AFTER applying pseudocounts ...')
        print()
        print('```{dot}')
        print(f'{hmm_to_dot(hmm)}')
        print('```')
        print()
        exploded = explode_hmm(
            hmm,
            source_state,
            sink_state,
            set(symbol for values in emission_probabilities.values() for symbol in values),
            emission_len,
            lambda g, state: g.get_node_data(state) != {}
        )
        print(f'The following exploded graph was produced for the HMM and an emission length of {emission_len} ...')
        print()
        print('```{dot}')
        print(f'{exploded_to_dot(exploded)}')
        print('```')
        print()
        probability = compute_exploded_max_emission_weights(
            hmm,
            exploded,
            lambda g, state, symbol: g.get_node_data(state)[symbol],
            lambda g, state: g.get_node_data(state) != {},
            lambda g, s1, s2: g.get_edge_data((s1, s2))
        )
        print(f'The following exploded graph forward and layer backtracking pointers were produced for the exploded graph...')
        print()
        print('```{dot}')
        print(f'{exploded_to_dot(exploded)}')
        print('```')
        print()
        emitted_seq = backtrack(
            hmm,
            exploded,
            lambda g, state: g.get_node_data(state) != {}
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
