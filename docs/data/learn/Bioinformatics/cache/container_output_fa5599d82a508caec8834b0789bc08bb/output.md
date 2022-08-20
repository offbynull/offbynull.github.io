<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

What's actually going on here that makes this work? Recall that the ...

* first column is sorted by symbol and symbol instance count (e.g. [¶1, a1, a2, a3, a4, b1, b2, ...]).
* last column guarantees that, for each symbol, that symbol's instances may be scattered around but are sorted if you only consider them by themselves (e.g. "b5" appears after "b4", but there are a bunch of other values in between them).

Knowing this, consider the 2nd range isolation step. When the first column is between "a1" and "a4", the range is limited to those 4 rows. Those 4 rows are then searched to see which has a last column with symbol "b". Of the "b" symbol instances found, ...

* the one with the min symbol instance count will be above the other "b" symbol instances.
* the one with the max symbol instance count will be below the other "b" symbol instances.
* the ones between them will have incrementing symbol instance by order of appearance.

For those 4 rows, the last column has "b1" in row 3 and "b2" in row 4, so the next range was isolated between first column being between "b1" and "b2". All rows in this next range are guaranteed to be for substrings that end with "a".

The point being that the "b" symbol instance counts aren't scattered / random, instead they're guaranteed to _increment by one_ as they appear down the last column. That's why isolating the next range between `min_symbol_instance_count("b")` and `max_symbol_instance_count("b")` works. Those "b" symbol instance counts, when you search for them in the first column, are guaranteed to be contiguous rows in the BWT table.

For example, imagine what would happen if the last column were ...

 * [b2, b3, b4, b5] - the rows where `first_col=[b2,b3,b4,b5]` are contiguous rows.
 * [b2, ?, b3, b4] - the rows where `first_col=[b2,b3,b4]` are contiguous rows.
 * [b3, ?, ?, b4] - the rows where `first_col=[b3,b4]` are contiguous rows.
 * [?, b3, ?, b4] - the rows where `first_col=[b3,b4]` are contiguous rows.
 * [b2, ?, ?, b3] - the rows where `first_col=[b2,b3]` are contiguous rows.
 * [?, b2, ?, ?] - the rows where `first_col=[b2]` are contiguous rows.

In contrast, the following last column scenarios will never happen ...

 * [b3, ?, ?, b2] - top-most "b" symbol instance doesn't have the min symbol instance count of all "b"s.
 * [b2, ?, ?, b2] - same "b" symbol instance will never appear twice.
 * [b5, b4, ?, b3] - "b" symbol instances must increment as they go top to bottom, not decrement.
 * [b4, b5, ?, b3] - "b" symbol instances must increment as they go top to bottom, not scatter.
</div>

