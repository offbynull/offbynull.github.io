import math
from collections import defaultdict
from sys import stdin
from typing import TypeVar, Iterable, Callable

import yaml

from graph.DirectedGraph import Graph


N = TypeVar('N')
ND = TypeVar('ND')
E = TypeVar('E')
ED = TypeVar('ED')
STATE = TypeVar('STATE')
SYMBOL = TypeVar('SYMBOL')


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


# MARKDOWN_DERIVE_TRANSITION_PROBS
def derive_transition_probabilities(
        hmm: Graph[N, ND, E, ED],
        list_state_transitions: Callable[[Graph[N, ND, E, ED]], Iterable[tuple[STATE, STATE]]],
        observed_transitions: list[tuple[STATE, STATE]]
) -> dict[tuple[STATE, STATE], float]:
    transition_counts = defaultdict(lambda: 0)
    transition_source_counts = defaultdict(lambda: 0)
    for src, dst in observed_transitions:
        transition_counts[src, dst] += 1
        transition_source_counts[src] += 1
    transition_probabilities = {}
    for src, dst in list_state_transitions(hmm):  # Query HMM for transitions (observed_transitions might miss some)
        if transition_source_counts[src] > 0:
            prob = transition_counts[src, dst] / transition_source_counts[src]
        else:
            prob = 0.0
        transition_probabilities[src, dst] = prob
    return transition_probabilities
# MARKDOWN_DERIVE_TRANSITION_PROBS


# MARKDOWN_DERIVE_EMISSION_PROBS
def derive_emission_probabilities(
        hmm: Graph[N, ND, E, ED],
        list_states: [[Graph[N, ND, E, ED]], Iterable[STATE]],
        list_symbols: [[Graph[N, ND, E, ED]], Iterable[SYMBOL]],
        get_node_emittable: Callable[[Graph[N, ND, E, ED], STATE], bool],
        observed_emissions: list[tuple[STATE, SYMBOL | None]]
) -> dict[tuple[STATE, SYMBOL], float]:
    dst_emission_counts = defaultdict(lambda: 0)
    dst_total_emission_counts = defaultdict(lambda: 0)
    for dst, symbol in observed_emissions:
        dst_emission_counts[dst, symbol] += 1
        dst_total_emission_counts[dst] += 1
    emission_probabilities = {}
    for dst in list_states(hmm):  # Query HMM for states (observed_emissions might miss some)
        if not get_node_emittable(hmm, dst):
            continue
        for symbol in list_symbols(hmm):
            if dst_total_emission_counts[dst] > 0:
                prob = dst_emission_counts[dst, symbol] / dst_total_emission_counts[dst]
            else:
                prob = 0.0
            emission_probabilities[dst, symbol] = prob
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
            lambda hmm: [(src, dst) for src, dsts in transitions.items() for dst in dsts],
            [(x[0], x[1]) for x in observed]
        )
        emission_probs = derive_emission_probabilities(
            hmm,
            lambda hmm: [state for state in transitions],
            lambda hmm: {symbol for dst, symbols in emissions.items() for symbol in symbols},
            lambda g, state: g.get_node_data(state) != {},
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
    # Assume first transition always begins from the SOURCE hidden state -- add it as non-emitting hidden state
    source_state = observed_sequence[0][0]
    non_emitting_hidden_states.add(source_state)
    # Ensure nothing conflicts
    if emitting_hidden_states & non_emitting_hidden_states != set():
        raise ValueError('Some states are reportedly non-emitting and emitting at the same time')
    # Build out HMM structure
    transitions = {}
    transitions[source_state] = non_emitting_hidden_states | emitting_hidden_states
    for state in non_emitting_hidden_states | emitting_hidden_states:
        transitions[state] = non_emitting_hidden_states | emitting_hidden_states
    emissions = {}
    for state in emitting_hidden_states:
        emissions[state] = symbols.copy()
    for state in non_emitting_hidden_states:
        emissions[state] = {}
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
            lambda hmm: [(src, dst) for src, dsts in transitions.items() for dst in dsts],
            [(x[0], x[1]) for x in observed]
        )
        emission_probs = derive_emission_probabilities(
            hmm,
            lambda hmm: [state for state in transitions],
            lambda hmm: {symbol for dst, symbols in emissions.items() for symbol in symbols},
            lambda g, state: g.get_node_data(state) != {},
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
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main_derive_hmm_structure()