from itertools import product


# SINK = 1.0
def backward_sink():
    for sink_weight in {0.151, 1.0}:
        yield [f'SINK: {sink_weight=}'], sink_weight


# A1 = SINK*{0.5,1.0}*0.7
def backward_A1():
    # Edge weight coming from sink may be 0.5 or 1.0
    # Try all emission probabilities
    for (trace, sink_weight), edge_weight, emission_prob in product(backward_sink(), {0.5, 1.0}, {0.3, 0.7, 0.1, 0.9}):
        yield trace + [f'>A1: {edge_weight=} {emission_prob=}'], sink_weight * edge_weight * emission_prob
    yield [f'>A1: Fake to 1.0'], 1.0


# B1 = SINK*{0.5,1.0}*0.9
def backward_B1():
    # Edge weight coming from sink may be 0.5 or 1.0
    # Try all emission probabilities
    for (trace, sink_weight), edge_weight, emission_prob in product(backward_sink(), {0.5, 1.0}, {0.3, 0.7, 0.1, 0.9}):
        yield trace + [f'>B1: {edge_weight=} {emission_prob=}'], sink_weight * edge_weight * emission_prob
    yield [f'>B1: Fake to 1.0'], 1.0


# A0 = A1*{0.9,0.2,0.1,0.8}+B1*{0.9,0.2,0.1,0.8}*0.3
def backward_A0():
    for (trace_a1, a1_weight), a1_edge_weight, (trace_b1, b1_weight), b1_edge_weight, emission_prob in product(backward_A1(), {0.9, 0.2, 0.1, 0.8}, backward_B1(), {0.9, 0.2, 0.1, 0.8}, {0.3, 0.7, 0.1, 0.9}):
        yield trace_a1 + trace_b1 + [f'>>A0: {a1_weight=} {a1_edge_weight=} {b1_weight=} {b1_edge_weight=} {emission_prob=}'], (a1_weight * a1_edge_weight + b1_weight * b1_edge_weight) * emission_prob


# A0 = A1*{0.9,0.2,0.1,0.8}+B1*{0.9,0.2,0.1,0.8}*0.3
def backward_B0():
    for (trace_a1, a1_weight), a1_edge_weight, (trace_b1, b1_weight), b1_edge_weight, emission_prob in product(backward_A1(), {0.9, 0.2, 0.1, 0.8}, backward_B1(), {0.9, 0.2, 0.1, 0.8}, {0.3, 0.7, 0.1, 0.9}):
        yield trace_a1 + trace_b1 + [f'>>A0: {a1_weight=} {a1_edge_weight=} {b1_weight=} {b1_edge_weight=} {emission_prob=}'], (a1_weight * a1_edge_weight + b1_weight * b1_edge_weight) * emission_prob


def forward_source():
    for source_weight in {1.0}:
        yield [f'SOURCE: {source_weight=}'], source_weight


def forward_A0():
    # Edge weight coming from sink may be 0.5 or 1.0
    # Try all emission probabilities
    for (trace, sink_weight), edge_weight, emission_prob in product(forward_source(), {0.5}, {0.3, 0.7, 0.1, 0.9}):
        yield trace + [f'>A0: {edge_weight=} {emission_prob=}'], sink_weight * edge_weight * emission_prob


def forward_B0():
    # Edge weight coming from sink may be 0.5 or 1.0
    # Try all emission probabilities
    for (trace, sink_weight), edge_weight, emission_prob in product(forward_source(), {0.5}, {0.3, 0.7, 0.1, 0.9}):
        yield trace + [f'>B0: {edge_weight=} {emission_prob=}'], sink_weight * edge_weight * emission_prob


for (forward_a0_trace, forward_a0), (backward_a0_trace, backward_a0) in product(forward_A0(), backward_A0()):
    v = forward_a0 * backward_a0 / 0.151
    if v >= 0.7145 and v <= 0.7154:
        print()
        print('FORWARD_A0_TRACE')
        print("\n".join(forward_a0_trace))
        print('BACKWARD_A0_TRACE')
        print("\n".join(backward_a0_trace))
        print(f'>>> {v} ({forward_a0=} {backward_a0=})')
# for (forward_b0_trace, forward_b0), (backward_b0_trace, backward_b0) in product(forward_B0(), backward_B0()):
#     v = forward_b0 * backward_b0 / 0.151
#     if v >= 0.2845 and v <= 0.2854:
#         print()
#         print('FORWARD_B0_TRACE')
#         print("\n".join(forward_b0_trace))
#         print('BACKWARD_B0_TRACE')
#         print("\n".join(backward_b0_trace))
#         print(f'>>> {v} ({forward_b0=} {backward_b0=})')

# for trace, v in A0():
#     if v > 0.714 and v < 0.725:
#         print()
#         print("\n".join(trace))
#         print(f'>>> {v}')


# for trace, v in B0():
#     if v > 0.854 and v < 0.865:
#         print()
#         print("\n".join(trace))
#         print(f'>>> {v}')


# for x, y in product({0.9, 0.2, 0.1, 0.8, 1.0}, {0.3, 0.7, 0.1, 0.9, 1.0}):
#     print(f'{x*y=}')