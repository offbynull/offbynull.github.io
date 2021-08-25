```python
def segregate_leaves(self, internal_edge: E) -> dict[N, N]:
    leaf_to_end = {}  # leaf -> one of the ends of internal_edge
    e1, e2 = self.tree.get_edge_ends(internal_edge)
    for l1 in self.leaf_nodes:
        # If path from l1 to e1 ends with internal_edge, it means that it had to
        # walk over the internal edge to get to e1, which ultimately means that l1
        # it isn't on the e1 side / it's on the e2 side. Otherwise, it's on the e1
        # side.
        p = self.path(l1, e1)
        if p[-1] != internal_edge:
            leaf_to_end[l1] = e1
        else:
            leaf_to_end[l1] = e2
    return leaf_to_end
```