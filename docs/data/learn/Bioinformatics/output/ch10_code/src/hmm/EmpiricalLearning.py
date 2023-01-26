import math
from collections import defaultdict
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


# MARKDOWN_DERIVE_TRANSITION_PROBS
def derive_transition_probabilities(
        hmm: Graph[STATE, HmmNodeData, TRANSITION, HmmEdgeData],
        observed_transitions: list[tuple[STATE, STATE]]
) -> dict[tuple[STATE, STATE], float]:
    transition_counts = defaultdict(lambda: 0)
    transition_source_counts = defaultdict(lambda: 0)
    for from_state, to_state in observed_transitions:
        transition_counts[from_state, to_state] += 1
        transition_source_counts[from_state] += 1
    transition_probabilities = {}
    for transition in hmm.get_edges():  # Query HMM for transitions (observed_transitions might miss some)
        from_state, to_state = transition
        if transition_source_counts[from_state] > 0:
            prob = transition_counts[from_state, to_state] / transition_source_counts[from_state]
        else:
            prob = 0.0
        transition_probabilities[from_state, to_state] = prob
    return transition_probabilities
# MARKDOWN_DERIVE_TRANSITION_PROBS


# MARKDOWN_DERIVE_EMISSION_PROBS
def derive_emission_probabilities(
        hmm: Graph[STATE, HmmNodeData, TRANSITION, HmmEdgeData],
        observed_emissions: list[tuple[STATE, SYMBOL | None]]
) -> dict[tuple[STATE, SYMBOL], float]:
    dst_emission_counts = defaultdict(lambda: 0)
    dst_total_emission_counts = defaultdict(lambda: 0)
    for to_state, symbol in observed_emissions:
        dst_emission_counts[to_state, symbol] += 1
        dst_total_emission_counts[to_state] += 1
    emission_probabilities = {}
    all_possible_symbols = {symbol for _, symbol in observed_emissions if symbol is not None}
    for to_state in hmm.get_nodes():  # Query HMM for states (observed_emissions might miss some)
        if not hmm.get_node_data(to_state).is_emittable():
            continue
        for symbol in all_possible_symbols:
            if dst_total_emission_counts[to_state] > 0:
                prob = dst_emission_counts[to_state, symbol] / dst_total_emission_counts[to_state]
            else:
                prob = 0.0
            emission_probabilities[to_state, symbol] = prob
    return emission_probabilities
# MARKDOWN_DERIVE_EMISSION_PROBS


def main_derive_probabilities():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        data_raw = ''.join(stdin.readlines())
        data: dict = yaml.safe_load(data_raw)
        transitions = {k: set(v) for k, v in data['transitions'].items()}
        emissions = {k: set(v) for k, v in data['emissions'].items()}
        observed = [tuple(x) for x in data['observed']]
        pseudocount = data['pseudocount']
        print(f'Deriving HMM probabilities using the following settings...')
        print()
        print('```')
        print(data_raw)
        print('```')
        print()
        transition_probs = {}
        for src, dsts in transitions.items():
            transition_probs[src] = {dst: math.nan for dst in dsts}
        emission_probs = {}
        for src, syms in emissions.items():
            emission_probs[src] = {sym: math.nan for sym in syms}
        hmm = to_hmm_graph_PRE_PSEUDOCOUNTS(transition_probs, emission_probs)
        print(f'The following HMM was produced (no probabilities) ...')
        print()
        print('```{dot}')
        print(f'{hmm_to_dot(hmm)}')
        print('```')
        print()
        print(f'The following probabilities were derived from the observed sequence of transitions and emissions ...')
        transition_probs = derive_transition_probabilities(
            hmm,
            [(x[0], x[1]) for x in observed]
        )
        emission_probs = derive_emission_probabilities(
            hmm,
            [(x[1], x[2] if len(x) == 3 else None) for x in observed]
        )
        print()
        print(f' * Transition probabilities:')
        for (from_state, to_state), prob in transition_probs.items():
            print(f'   * {from_state}→{to_state} = {prob}')
        print()
        print(f' * Emission probabilities:')
        for (to_state, to_symbol), prob in emission_probs.items():
            print(f'   * ({to_state}, {to_symbol}) = {prob}')
        print()
        print(f'The following HMM was produced after derived probabilities were applied ...')
        transition_probs_for_hmm = {}
        for (src, dst), weight in transition_probs.items():
            if src not in transition_probs_for_hmm:
                transition_probs_for_hmm[src] = {}
            transition_probs_for_hmm[src][dst] = weight
        symbols = {symbol for dst, symbols in emissions.items() for symbol in symbols}
        emission_probs_for_hmm = {}
        for dst in transitions:
            for symbol in symbols:
                if dst not in emission_probs_for_hmm:
                    emission_probs_for_hmm[dst] = {}
                weight = emission_probs.get((dst, symbol), None)
                if weight is not None:
                    emission_probs_for_hmm[dst][symbol] = weight
        hmm = to_hmm_graph_PRE_PSEUDOCOUNTS(transition_probs_for_hmm, emission_probs_for_hmm)
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
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")













# MARKDOWN_DERIVE_HMM_STRUCTURE
def derive_hmm_structure(
        observed_sequence: list[tuple[STATE, STATE, SYMBOL] | tuple[STATE, STATE]]
) -> tuple[
    dict[STATE, set[STATE]],  # hidden state-hidden state transitions
    dict[STATE, set[SYMBOL]]  # hidden state-symbol emission transitions
]:
    symbols = set()
    emitting_hidden_states = set()
    non_emitting_hidden_states = set()
    # Walk entries in observed sequence
    for entry in observed_sequence:
        if len(entry) == 3:
            from_state, to_state, to_symbol = entry
            symbols.add(to_symbol)
            emitting_hidden_states.add(to_state)
        else:
            from_state, to_state = entry
            non_emitting_hidden_states.add(to_state)
    # Unable to infer when there are non-emitting hidden states. Recall that non-emitting hidden states cannot form
    # cycles because those cycles will infinitely blow out when exploding out an HMM (Viterbi). When there's only one
    # non-emitting hidden state, it's fine so long as you kill the edge to itself. When there's more than one
    # non-emitting hidden state, this algorithm assumes that they can point at each other, which will cause a cycle.
    #
    # For example, if there are two non-emitting states A and B, this algorithm will always produce a cycle.
    # .----.
    # |    v
    # A<---B
    #
    # The observed sequence doesn't make it clear which of thw two edges should be kept vs which should be discarded. As
    # such, non-emitting hidden states (other than the SOURCE state) aren't allowed in this algorithm.
    if non_emitting_hidden_states:
        raise ValueError('Cannot derive HMM structure when there are non-emitting hidden sates')
    # Assume first transition always begins from the SOURCE hidden state -- add it as non-emitting hidden state
    source_state = observed_sequence[0][0]
    # Build out HMM structure
    transitions = {}
    transitions[source_state] = emitting_hidden_states.copy()
    for state in emitting_hidden_states:
        transitions[state] = emitting_hidden_states.copy()
    emissions = {}
    emissions[source_state] = {}
    for state in emitting_hidden_states:
        emissions[state] = symbols.copy()
    return transitions, emissions
# MARKDOWN_DERIVE_HMM_STRUCTURE


def main_derive_hmm_structure():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        data_raw = ''.join(stdin.readlines())
        data: dict = yaml.safe_load(data_raw)
        observed = [tuple(x) for x in data['observed']]
        pseudocount = data['pseudocount']
        print(f'Deriving HMM probabilities into assumed HMM structure using the following settings...')
        print()
        print('```')
        print(data_raw)
        print('```')
        print()
        transitions, emissions = derive_hmm_structure(observed)
        print(f'The following HMM hidden state transitions and symbol emissions were assumed...')
        print()
        print(f' * {transitions=}')
        print(f' * {emissions=}')
        print()
        transition_probs = {}
        for src, dsts in transitions.items():
            transition_probs[src] = {dst: math.nan for dst in dsts}
        emission_probs = {}
        for src, syms in emissions.items():
            emission_probs[src] = {sym: math.nan for sym in syms}
        hmm = to_hmm_graph_PRE_PSEUDOCOUNTS(transition_probs, emission_probs)
        print(f'The following HMM was produced (no probabilities) ...')
        print()
        print('```{dot}')
        print(f'{hmm_to_dot(hmm)}')
        print('```')
        print()
        print(f'The following probabilities were derived from the observed sequence of transitions and emissions ...')
        transition_probs = derive_transition_probabilities(
            hmm,
            [(x[0], x[1]) for x in observed]
        )
        emission_probs = derive_emission_probabilities(
            hmm,
            [(x[1], x[2] if len(x) == 3 else None) for x in observed]
        )
        print()
        print(f' * {transition_probs=}')
        print(f' * {emission_probs=}')
        print()
        print(f'The following HMM was produced after derived probabilities were applied ...')
        transition_probs_for_hmm = {}
        for (src, dst), weight in transition_probs.items():
            if src not in transition_probs_for_hmm:
                transition_probs_for_hmm[src] = {}
            transition_probs_for_hmm[src][dst] = weight
        symbols = {symbol for dst, symbols in emissions.items() for symbol in symbols}
        emission_probs_for_hmm = {}
        for dst in transitions:
            for symbol in symbols:
                if dst not in emission_probs_for_hmm:
                    emission_probs_for_hmm[dst] = {}
                weight = emission_probs.get((dst, symbol), None)
                if weight is not None:
                    emission_probs_for_hmm[dst][symbol] = weight
        hmm = to_hmm_graph_PRE_PSEUDOCOUNTS(transition_probs_for_hmm, emission_probs_for_hmm)
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
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main_derive_hmm_structure()
