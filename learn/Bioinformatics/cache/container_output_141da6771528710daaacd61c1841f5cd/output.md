<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

I'm thinking that the probability isn't what you want here. Instead what you want is likely just the distances themselves or the distances normalized between 0 and 1: `{kt} \frac{D_j}{\sum_{i=1}^n{D_i}}`. Those will allow you to figure out more interesting things about the clustering. For example, if a set of leaf nodes are all roughly the equidistant to the same internal node and that distance is greater than some threshold, they're likely things you should be interested in.
</div>

