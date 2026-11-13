<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

Recall the terminology used for BWT:

 * Symbol: A unique element within the sequence (e.g. "banana¶" is made up of the *unique elements* / *symbols* {a, b, n, ¶}).
 * Symbol instance: The occurrence of a symbol (e.g. index 4 of "banana¶" is the 2nd *occurrence* / *symbol instance* of *n*).
 * Symbol instance count: The occurrence number of a symbol instance (e.g. index 4 of "banana¶" is *n* and it *is occurrence number* / *has a symbol instance count of* 2).
 * `first_occurrence_map`: `first` collapsed such that only the index of each symbol's initial occurrence is retained (introduced in collapsed first algorithm).
 * `first_indexes`: A column where each row contains the index of the corresponding `first` row's symbol instance within the original sequence (introduced in checkpointed indexes algorithm).
 * `last_tallies`: A column where each row contains a tally of how many times each symbol `last` was encountered up until reaching that index (introduced in checkpointed ranks algorithm).
 * `last_to_first`: A column that, at each row, maps that row's `last` value to its index within `first` (removed in collapsed first algorithm, replaced with dynamic calculation).
 * BWT records: The table comprised of columns `first_indexes`, `last`, and `last_tallies` (updated in checkpointed ranks algorithm).
</div>

