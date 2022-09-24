<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

Recall the terminology used for BWT:

 * Symbol: A unique element within the sequence (e.g. "banana¶" is made up of the *unique elements* / *symbols* {a, b, n, ¶}).
 * Symbol instance: The occurrence of a symbol (e.g. index 4 of "banana¶" is the 2nd *occurrence* / *symbol instance* of *n*).
 * Symbol instance count: The occurrence number of a symbol instance (e.g. index 4 of "banana¶" is *n* and it *is occurrence number* / *has a symbol instance count of* 2).
 * `first`: The first column of a BWT matrix.
 * `last`: The last column of a BWT matrix.
 * `last_to_first`: A column that, at each row, maps that row's `last` value to its index within `first` (`last_to_first[i] = first.find(last[i])`).
 * BWT records: The table comprised of columns `first`, `last`, and `last_to_first`.
</div>

