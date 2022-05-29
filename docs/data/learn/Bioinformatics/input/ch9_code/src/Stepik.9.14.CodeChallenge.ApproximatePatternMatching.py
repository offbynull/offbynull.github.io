from sequence_search import SuffixArray, SuffixTree, Trie_Basic, Trie_AhoCorasick, Trie_EdgeMerged
from sequence_search.SearchUtils import StringView

with open('/home/user/Downloads/dataset_240387_10(1).txt', mode='r', encoding='utf-8') as f:
# with open('/home/user/Downloads/test.txt', mode='r', encoding='utf-8') as f:
    data = f.read()
data = [l.strip() for l in data.strip().split('\n')]
text = data[0].strip()
patterns = data[1].strip().split()
max_mismatch = int(data[2].strip())

# At this question, I stopped and implemented clean versions of the algorithms -- this question uses those clean
# versions.

# WARNING: The padding logic was added AFTER answering the question. That means this code my fail with a new dataset
# because the grader isn't expecting the code to pad.

end_marker_sv = StringView.wrap('$')
pad_marker_sv = StringView.wrap('!')
text_sv = StringView.wrap(text)
patterns_sv = set(StringView.wrap(p) for p in patterns)
found = {p: [] for p in patterns_sv}
# _, matched_set = Trie_Basic.mismatch_search(text_sv, patterns_sv, max_mismatch, end_marker_sv, pad_marker_sv)
# _, matched_set = Trie_AhoCorasick.mismatch_search(text_sv, patterns_sv, max_mismatch, end_marker_sv, pad_marker_sv)
# _, matched_set = Trie_EdgeMerged.mismatch_search(text_sv, patterns_sv, max_mismatch, end_marker_sv, pad_marker_sv)
# _, matched_set = SuffixTree.mismatch_search(text_sv, patterns_sv, max_mismatch, end_marker_sv, pad_marker_sv)
_, matched_set = SuffixArray.mismatch_search(text_sv, patterns_sv, max_mismatch, end_marker_sv, pad_marker_sv)
for test_seq_idx, search_seq, found_value, dist in matched_set:
    found[search_seq].append(test_seq_idx)

for k, v in found.items():
    print(f'{k}: {" ".join(str(s) for s in v)}')
