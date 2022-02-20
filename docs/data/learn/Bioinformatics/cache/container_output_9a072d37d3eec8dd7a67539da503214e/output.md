<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

Recall that neighbour joining phylogeny doesn't reconstruct a rooted tree because distance matrices don't capture hierarchy information. Also recall that edges broken up by a node (internal nodes of degree_GRAPH 2) also aren't reconstructed because distance matrices don't capture that information either. If the original tree that the distance matrix is for was a rooted tree but the root node only had two children, that node won't show up at all in the reconstructed tree (simple tree).

```{svgbob}
ORIGINAL           RECONSTRUCTED   

   R (root)             2
1 / \ 1              A-----B
 /   \
A     B
```

In the example above, the root node had degree_GRAPH of 2, meaning it won't appear in reconstructed simple tree. Even if it did, the reconstruction would be unrooted tree -- the node would be there but nothing would identify it as the root.
</div>

