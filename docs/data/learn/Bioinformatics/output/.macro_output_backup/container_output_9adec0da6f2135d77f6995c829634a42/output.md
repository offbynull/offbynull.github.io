<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

Other than the v5's limb, I think no other edge in the graph should ever have a weight of 0. That's why this will always be >, because each traverses more edges to get to v5 than they do to get to each other, and those edges have positive weights (not zero).

A edge weight of 0 means the species on both sides of an edge are the same, which should never be case (why have an edge at all then? why not merge the edge into a single node? they represent the same thing). v5's limb is explicitly being set to 0 because it's a temporary thing the algorithm requires.
</div>

