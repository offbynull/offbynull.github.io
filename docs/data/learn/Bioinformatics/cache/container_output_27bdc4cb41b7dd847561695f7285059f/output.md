<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

Recall the terminology used for BWT:

 * Symbol: A unique element within the sequence (e.g. "banana¶" is made up of the *unique elements* / *symbols* {a, b, n, ¶}).
 * Symbol instance: The occurrence of a symbol (e.g. index 4 of "banana¶" is the 2nd *occurrence* / *symbol instance* of *n*).
 * Symbol instance count: The occurrence number of a symbol instance (e.g. index 4 of "banana¶" is *n* and it *is occurrence number* / *has a symbol instance count of* 2).
 * `first`: The first column of a BWT matrix (removed in collapsed first algorithm, replaced with `first_occurrence_map`).
 * `first_occurrence_map`: `first` collapsed such that only the index of each symbol's initial occurrence is retained (introduced in collapsed first algorithm).
 * `last`: The last column of a BWT matrix.
 * BWT records: The table comprised of just the column `last` (updated in collapsed first algorithm).
</div>

