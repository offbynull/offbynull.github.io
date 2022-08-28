<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

Recall the property of the last column of the BWT matrix as well: For each symbol, that symbol's instances may be scattered around but are sorted if you only consider them by themselves. For example, `{h}#f00 (a,1)` appears before `{h}#b00 (a,2)` but there are a bunch of other values in between.

This is an important point to understanding why this algorithm works, explained in a note further below.
</div>

