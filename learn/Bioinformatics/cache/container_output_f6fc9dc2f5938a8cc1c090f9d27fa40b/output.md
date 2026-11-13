<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

The other types of sequence alignment detailed in the sibling sections below don't implement a version of this algorithm. It's fairly straight forward to adapt this algorithm to support those sequence alignment types, but I didn't have the time to do it -- I almost completed a local alignment version but backed out. The same high-level logic applies to those other alignment types: Converge on positions to find nodes/edges in the maximal alignment path and sub-divide on those positions.
</div>

