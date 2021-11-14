<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

The Pevzner book says to pick an edge and inject a fake root into it, then remove it once the sequences have been inferred. I can't see how doing that is any better than just picking some internal node to be the root.

So which node should be selected as root? The tree structure being used for this algorithm very likely came from a phylogenetic tree built using distances (e.g. additive phylogeny, neighbour joining phylogeny, UPGMA, etc..). Here are a couple of ideas I just thought up: 

 * For each leaf node, count the number of nodes in the path to reach that internal node. Sum up the counts and pick the internal node with the largest sum as the root.
 * For each leaf node, calculate the distance to reach that internal node. Sum up the distances and pick the internal node with the largest sum as the root.

I think the second one might not work because all sums will be the same? Maybe instead average the distances to leaf nodes and pick the one with the largest average?
</div>

