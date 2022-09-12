<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

What's actually going on here that makes this work? Recall that the ...

* first column is sorted by symbol and symbol instance count (e.g. [(¶,1), (a,1), (a,2), (a,3), (a,4), (b,1), (b,2), ...]).
* last column guarantees that, for each symbol, that symbol's instances may be scattered around but are sorted if you only consider them by themselves (e.g. (b,5) appears after (b,4), but there are a bunch of other values in between them).

Knowing this, consider the 2nd range isolation step. When the first column is between (a,1) and (a,4), the range is limited to those 4 rows. Those 4 rows are then searched to see which has a last column with symbol *b*. Of the *b* symbol instances found, ...

* the one with the min symbol instance count will be above the other *b* symbol instances.
* the one with the max symbol instance count will be below the other *b* symbol instances.
* the ones between them will have incrementing symbol instance by order of appearance.

For those 4 rows, the last column has (b,1) in row 3 and (b,2) in row 4, so the next range was isolated between first column being between (b,1) and (b,2). All rows in this next range are guaranteed to be for substrings that end with *a*.

The point being that the *b* symbol instance counts aren't scattered / random, instead they're guaranteed to _increment by one_ as they appear down the last column. That's why isolating the next range between `min_symbol_instance_count(b)` and `max_symbol_instance_count(b)` works. Those *b* symbol instance counts, when you search for them in the first column, are guaranteed to be contiguous rows in the BWT table.

For example, imagine what would happen if the last column were ...

 * [(b,2), (b,3), (b,4), (b,5)] - the rows where `first_col=[('b',2),('b',3),('b',4),('b',5)]` are contiguous rows.
 * [(b,2), ?,     (b,3), (b,4)] - the rows where `first_col=[('b',2),('b',3),('b',4)]` are contiguous rows.
 * [(b,3), ?,     ?,     (b,4)] - the rows where `first_col=[('b',3),('b',4)]` are contiguous rows.
 * [?,     (b,3), ?,     (b,4)] - the rows where `first_col=[('b',3),('b',4)]` are contiguous rows.
 * [(b,2), ?,     ?,     (b,3)] - the rows where `first_col=[('b',2),('b',3)]` are contiguous rows.
 * [?,     (b,2), ?,     ?    ] - the rows where `first_col=[('b',2)]` are contiguous rows.

In contrast, the following last column scenarios will never happen ...

 * [(b,3), ?,     ?, (b,2)] - top-most *b* symbol instance doesn't have the min symbol instance count of all *b*s.
 * [(b,2), ?,     ?, (b,2)] - same *b* symbol instance will never appear twice.
 * [(b,5), (b,4), ?, (b,3)] - *b* symbol instances must increment as they go top to bottom, not decrement.
 * [(b,4), (b,5), ?, (b,3)] - *b* symbol instances must increment as they go top to bottom, not scatter.
</div>

