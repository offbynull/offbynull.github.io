from typing import TypeVar, Any

from hmm.MostProbableHiddenPath_ViterbiNonEmittingHiddenStates import to_hmm_graph_PRE_PSEUDOCOUNTS, hmm_to_dot

ELEM = TypeVar('ELEM')


def create_hmm_square(
        transition_probabilities: dict[str, dict[str, float]],
        emission_probabilities: dict[str, dict[str, float]],
        hmm_from_n_id: Any,
        v_elem: tuple[int, ELEM],
        w_elem: tuple[int, ELEM]
):
    if f'{hmm_from_n_id}' not in transition_probabilities:
        transition_probabilities[f'{hmm_from_n_id}'] = {}
        emission_probabilities[f'{hmm_from_n_id}'] = {}

    hmm_to_n_id = 'D', v_elem[0], w_elem[0] + 1
    if f'{hmm_to_n_id}' not in transition_probabilities:
        transition_probabilities[f'{hmm_to_n_id}'] = {}
        emission_probabilities[f'{hmm_to_n_id}'] = {}
    transition_probabilities[f'{hmm_from_n_id}'][f'{hmm_to_n_id}'] = 0.0

    hmm_to_n_id = 'E', v_elem[0] + 1, w_elem[0]
    if f'{hmm_to_n_id}' not in transition_probabilities:
        transition_probabilities[f'{hmm_to_n_id}'] = {}
        emission_probabilities[f'{hmm_to_n_id}'] = {}
    transition_probabilities[f'{hmm_from_n_id}'][f'{hmm_to_n_id}'] = 0.0
    emission_probabilities[f'{hmm_to_n_id}']['?'] = 1.0

    hmm_to_n_id = 'E', v_elem[0] + 1, w_elem[0] + 1
    if f'{hmm_to_n_id}' not in transition_probabilities:
        transition_probabilities[f'{hmm_to_n_id}'] = {}
        emission_probabilities[f'{hmm_to_n_id}'] = {}
    transition_probabilities[f'{hmm_from_n_id}'][f'{hmm_to_n_id}'] = 0.0
    emission_probabilities[f'{hmm_to_n_id}']['?'] = 1.0

    hmm_from_n_id = 'E', v_elem[0] + 1, w_elem[0]
    if f'{hmm_from_n_id}' not in transition_probabilities:
        transition_probabilities[f'{hmm_from_n_id}'] = {}
        emission_probabilities[f'{hmm_from_n_id}'] = {}
    hmm_to_n_id = 'D', v_elem[0] + 1, w_elem[0] + 1
    if f'{hmm_to_n_id}' not in transition_probabilities:
        transition_probabilities[f'{hmm_to_n_id}'] = {}
        emission_probabilities[f'{hmm_to_n_id}'] = {}
    transition_probabilities[f'{hmm_from_n_id}'][f'{hmm_to_n_id}'] = 0.0

    hmm_from_n_id = 'D', v_elem[0], w_elem[0] + 1
    if f'{hmm_from_n_id}' not in transition_probabilities:
        transition_probabilities[f'{hmm_from_n_id}'] = {}
        emission_probabilities[f'{hmm_from_n_id}'] = {}
    hmm_to_n_id = 'E', v_elem[0] + 1, w_elem[0] + 1
    transition_probabilities[f'{hmm_from_n_id}'][f'{hmm_to_n_id}'] = 0.0


transition_probabilities = {}
emission_probabilities = {}
create_hmm_square(
    transition_probabilities,
    emission_probabilities,
    'S',
    (0, 'n'),
    (0, 'a')
)

g = to_hmm_graph_PRE_PSEUDOCOUNTS(transition_probabilities, emission_probabilities)

print(hmm_to_dot(g))
