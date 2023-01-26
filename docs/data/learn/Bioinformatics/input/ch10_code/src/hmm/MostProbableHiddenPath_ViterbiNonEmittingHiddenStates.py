import math
from sys import stdin
from typing import TypeVar, Iterator, Protocol, Any

import yaml

from find_max_path import FindMaxPath_DPBacktrack
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


# MARKDOWN
VITERBI_NODE_ID = tuple[int, STATE]
VITERBI_EDGE_ID = tuple[VITERBI_NODE_ID, VITERBI_NODE_ID]


def to_viterbi_graph(
        hmm: Graph[STATE, HmmNodeData, TRANSITION, HmmEdgeData],
        hmm_source_n_id: STATE,
        hmm_sink_n_id: STATE,
        emissions: list[SYMBOL]
) -> Graph[VITERBI_NODE_ID, Any, VITERBI_EDGE_ID, float]:
    viterbi = Graph()
    # Add Viterbi source node.
    viterbi_source_n_id = -1, hmm_source_n_id
    viterbi.insert_node(viterbi_source_n_id)
    # Explode out HMM into Viterbi.
    viterbi_from_n_emissions_idx = -1
    viterbi_from_n_ids = {viterbi_source_n_id}
    viterbi_to_n_emissions_idx = 0
    viterbi_to_n_ids_emitting = set()
    viterbi_to_n_ids_non_emitting = set()
    while viterbi_from_n_ids and viterbi_to_n_emissions_idx < len(emissions):
        viterbi_to_n_symbol = emissions[viterbi_to_n_emissions_idx]
        viterbi_to_n_ids_emitting = set()
        viterbi_to_n_ids_non_emitting = set()
        while viterbi_from_n_ids:
            viterbi_from_n_id = viterbi_from_n_ids.pop()
            _, hmm_from_n_id = viterbi_from_n_id
            for _, _, hmm_to_n_id, _ in hmm.get_outputs_full(hmm_from_n_id):
                hmm_to_n_emittable = hmm.get_node_data(hmm_to_n_id).is_emittable()
                transition = hmm_from_n_id, hmm_to_n_id
                if hmm_to_n_emittable:
                    hidden_state_transition_prob = hmm.get_edge_data(transition).get_transition_probability()
                    symbol_emission_prob = hmm.get_node_data(hmm_to_n_id).get_symbol_emission_probability(viterbi_to_n_symbol)
                    viterbi_to_n_id = viterbi_to_n_emissions_idx, hmm_to_n_id
                    connect_viterbi_nodes(
                        viterbi,
                        viterbi_from_n_id,
                        viterbi_to_n_id,
                        hidden_state_transition_prob * symbol_emission_prob
                    )
                    viterbi_to_n_ids_emitting.add(viterbi_to_n_id)
                else:
                    hidden_state_transition_prob =  hmm.get_edge_data(transition).get_transition_probability()
                    viterbi_to_n_id = viterbi_from_n_emissions_idx, hmm_to_n_id
                    to_n_existed = connect_viterbi_nodes(
                        viterbi,
                        viterbi_from_n_id,
                        viterbi_to_n_id,
                        hidden_state_transition_prob
                    )
                    if not to_n_existed:
                        viterbi_from_n_ids.add(viterbi_to_n_id)
                    viterbi_to_n_ids_non_emitting.add(viterbi_to_n_id)
        viterbi_from_n_ids = viterbi_to_n_ids_emitting
        viterbi_from_n_emissions_idx += 1
        viterbi_to_n_emissions_idx += 1
    # Ensure all emitted symbols were consumed when exploding out to Viterbi.
    assert viterbi_to_n_emissions_idx == len(emissions)
    # Explode out the non-emitting hidden states of the final last emission index (does not happen in the above loop).
    viterbi_to_n_ids_non_emitting = set()
    viterbi_from_n_ids = viterbi_to_n_ids_emitting.copy()
    while viterbi_from_n_ids:
        viterbi_from_n_id = viterbi_from_n_ids.pop()
        _, hmm_from_n_id = viterbi_from_n_id
        for _, _, hmm_to_n_id, _ in hmm.get_outputs_full(hmm_from_n_id):
            hmm_to_n_emmitable = hmm.get_node_data(hmm_to_n_id).is_emittable()
            if hmm_to_n_emmitable:
                continue
            transition = hmm_from_n_id, hmm_to_n_id
            hidden_state_transition_prob = hmm.get_edge_data(transition).get_transition_probability()
            viterbi_to_n_id = viterbi_from_n_emissions_idx, hmm_to_n_id
            connect_viterbi_nodes(
                viterbi,
                viterbi_from_n_id,
                viterbi_to_n_id,
                hidden_state_transition_prob
            )
            viterbi_to_n_ids_non_emitting.add(viterbi_to_n_id)
            viterbi_from_n_ids.add(viterbi_to_n_id)
    # Add Viterbi sink node.
    viterbi_to_n_id = -1, hmm_sink_n_id
    for viterbi_from_n_id in viterbi_to_n_ids_emitting | viterbi_to_n_ids_non_emitting:
        connect_viterbi_nodes(viterbi, viterbi_from_n_id, viterbi_to_n_id, 1.0)
    return viterbi


def connect_viterbi_nodes(
        viterbi: Graph[VITERBI_NODE_ID, Any, VITERBI_EDGE_ID, float],
        viterbi_from_n_id: VITERBI_NODE_ID,
        viterbi_to_n_id: VITERBI_NODE_ID,
        weight: float
) -> bool:
    to_n_existed = True
    if not viterbi.has_node(viterbi_to_n_id):
        viterbi.insert_node(viterbi_to_n_id)
        to_n_existed = False
    viterbi_e_weight = weight
    viterbi_e_id = viterbi_from_n_id, viterbi_to_n_id
    viterbi.insert_edge(
        viterbi_e_id,
        viterbi_from_n_id,
        viterbi_to_n_id,
        viterbi_e_weight
    )
    return to_n_existed
# MARKDOWN


def viterbi_to_dot(g: Graph[VITERBI_NODE_ID, Any, VITERBI_EDGE_ID, float]) -> str:
    ret = 'digraph G {\n'
    ret += ' graph[rankdir=LR]\n'
    ret += ' node[shape=egg, fontname="Courier-Bold", fontsize=10]\n'
    ret += ' edge[fontname="Courier-Bold", fontsize=10]\n'
    for n in sorted(g.get_nodes()):
        ret += f'"{n}" [label="{n}"]\n'
    for e in sorted(g.get_edges()):
        n1, n2, weight = g.get_edge(e)
        ret += f'"{n1}" -> "{n2}" [label="{weight}"]\n'
    ret += '}'
    return ret


def max_product_path_in_viterbi(
        viterbi: Graph[VITERBI_NODE_ID, Any, VITERBI_EDGE_ID, float]
):
    # Backtrack to find path with max sum -- using logged weights, path with max sum is actually path with max product.
    # Note that the call to populate_weights_and_backtrack_pointers() below is taking the math.log() of the edge weight
    # rather than passing back the edge weight itself.
    source_n_id = viterbi.get_root_node()
    sink_n_id = viterbi.get_leaf_node()
    FindMaxPath_DPBacktrack.populate_weights_and_backtrack_pointers(
        viterbi,
        source_n_id,
        lambda n, w, e: viterbi.update_node_data(n, (w, e)),
        lambda n: viterbi.get_node_data(n),
        lambda e: -math.inf if viterbi.get_edge_data(e) == 0 else math.log(viterbi.get_edge_data(e)),
    )
    edges = FindMaxPath_DPBacktrack.backtrack(
        viterbi,
        sink_n_id,
        lambda n_id: viterbi.get_node_data(n_id)
    )
    path = []
    final_weight = 1.0
    for e_id in edges:
        _, from_node = viterbi.get_edge_from(e_id)
        _, to_node = viterbi.get_edge_to(e_id)
        path.append((from_node, to_node))
        weight = viterbi.get_edge_data(e_id)
        final_weight *= weight
    return final_weight, path


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
        print(f'Building Viterbi graph (with non-emitting hidden states) and finding the max product weight, after applying psuedocounts to HMM, using the following settings...')
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
        viterbi = to_viterbi_graph(
            hmm,
            source_state,
            sink_state,
            emissions
        )
        print(f'The following Viterbi graph was produced for the HMM and the emitted sequence {emissions} ...')
        print()
        print('```{dot}')
        print(f'{viterbi_to_dot(viterbi)}')
        print('```')
        print()
        weight, hidden_path = max_product_path_in_viterbi(viterbi)
        print(f'The hidden path with the max product weight in this Viterbi graph is {hidden_path} (max product weight = {weight}).')
        print()
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")







if __name__ == '__main__':
    main()
