import lzma

import matplotlib.pyplot as plt

from breakpoint_graph import LinearBreakpointGraph
from synteny_graph.Match import Match, MatchType
from synteny_graph.MatchMerger import distance_merge, overlap_filter, to_synteny_permutation
from synteny_graph.MatchOverlapClipper import Axis

with lzma.open('anchors_human_mouse.txt.xz', mode='rt', encoding='utf-8') as f:
    data = str(f.read())
lines = data.strip().split('\n')
lines = lines[1:]
matches = []
for line in lines:
    line = line.strip()
    row = line.split(' ')
    m = Match(
        y_axis_chromosome=row[1],
        y_axis_chromosome_min_idx=int(row[2]),
        y_axis_chromosome_max_idx=int(row[3]),
        x_axis_chromosome=row[4],
        x_axis_chromosome_min_idx=int(row[5]),
        x_axis_chromosome_max_idx=int(row[6]),
        type=MatchType.NORMAL if row[7] == '+' else MatchType.REVERSE_COMPLEMENT
    )
    matches.append(m)
lines = []  # no longer required -- clear out memory
# matches = [m for m in matches if m.y_axis_chromosome in {'1', '2'}]
# matches = [m for m in matches if m.x_axis_chromosome == '1']
# matches = random.sample(matches, len(matches) // 10)
print(f'{len(matches)}')
matches = distance_merge(matches, radius=10000)
print(f'{len(matches)}')
matches = distance_merge(matches, radius=20000)
print(f'{len(matches)}')
matches = distance_merge(matches, radius=30000)
print(f'{len(matches)}')
matches = distance_merge(matches, radius=40000)
print(f'{len(matches)}')
matches = distance_merge(matches, radius=50000)
print(f'{len(matches)}')
matches = distance_merge(matches, radius=60000)
print(f'{len(matches)}')
matches = distance_merge(matches, radius=70000)
print(f'{len(matches)}')
matches = distance_merge(matches, radius=80000)
print(f'{len(matches)}')
matches = distance_merge(matches, radius=90000)
print(f'{len(matches)}')
matches = distance_merge(matches, radius=100000)
print(f'{len(matches)}')
matches = [m for m in matches if m.length() >= 100000]
print(f'{len(matches)}')
matches = distance_merge(matches, radius=200000)
print(f'{len(matches)}')
matches = distance_merge(matches, radius=300000)
print(f'{len(matches)}')
matches = distance_merge(matches, radius=400000)
print(f'{len(matches)}')
matches = distance_merge(matches, radius=500000)
print(f'{len(matches)}')
matches = overlap_filter(matches, max_filter_length=1000000, max_merge_distance=5000000)
print(f'{len(matches)}')
human_perms, mouse_perms = to_synteny_permutation(matches, Axis.Y, synteny_prefix='HUMAN')
print(f'{human_perms}')
print(f'{mouse_perms}')

bg = LinearBreakpointGraph.BreakpointGraph(
    [mouse_perms[ch] for ch in sorted(mouse_perms.keys())],
    [human_perms[ch] for ch in sorted(human_perms.keys())]
)
print(bg.to_neato_graph())
print(f'{bg.get_red_permutations()}')
two_break_estimate = bg.two_break_distance()
two_break_counter = 0
while True:
    next_blue_edge_to_break_on = bg.find_blue_edge_in_non_trivial_path()
    if next_blue_edge_to_break_on is None:
        break
    bg.two_break(next_blue_edge_to_break_on)
    two_break_counter += 1
    print(f'{bg.get_red_permutations()}')
    print(bg.to_neato_graph())

print(f'actual 2 break count: {two_break_counter} vs estimated 2 break count: {two_break_estimate}')

Match.plot(matches, y_axis_organism_name='human', x_axis_organism_name='mouse')
plt.show()
