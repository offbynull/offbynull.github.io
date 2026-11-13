<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

From the book:

> Exercise Break: The algorithm proposed on the previous step computes LimbLength(j) in O(n2) time (for an n x n distance matrix). Design an algorithm that computes LimbLength(j) in O(n) time.

The answer to this is obvious now that I've gone through and reasoned about things above.

For the limb length formula to work, you need to find leaf nodes (A, B) whose path travels through leaf node L's parent (Lp). Originally, the book had you try all combinations of leaf nodes (L excluded) and take the minimum. That works, but you don't need to try all possible pairs. Instead, you can just pick any leaf (that isn't L) for A and test against every other node (that isn't L) to find B -- as with the original method, you pick the B that produces the minimum value.
   
Because a phylogenetic tree is a connected graph (a path exists between each node and all other nodes), at least 1 path will exist starting from A that travels through Lp.

```python
leaf_nodes.remove(L)  # remove L from the set
A = leaf_nodes.pop()  # removes and returns an arbitrary leaf node
B = min(leafs, key=lambda x: (dist(L, A) + dist(L, x) - dist(A, x)) / 2)
```

For example, imagine that you're trying to find v2's limb length in the following graph...

```{dot}
graph G {
 graph[rankdir=LR]
 node[shape=circle, fontname="Courier-Bold", fontsize=10, width=0.4, height=0.4, fixedsize=true]
 edge[arrowsize=0.6, fontname="Courier-Bold", fontsize=10, arrowhead=vee]
 subgraph cluster_one {
  fontname="Courier-Bold"
  fontsize=10
  v0 -- i0
  v1 -- i0
  i0 -- i1
  v2 -- i1
  v3 -- i1
  i1 -- i2
  v4 -- i2
  i2 -- i3
  i3 -- v5
  i3 -- v6
 }
}
```

Pick v4 as your A node, then try the formula with every other leaf node as B (except v2 because that's the node you're trying to get limb length for + v4 because that's your A node). At least one of path(A, B)'s will cross through v2's parent. Take the minimum, just as you did when you were trying every possible node pair across all leaf nodes in the graph.
</div>

