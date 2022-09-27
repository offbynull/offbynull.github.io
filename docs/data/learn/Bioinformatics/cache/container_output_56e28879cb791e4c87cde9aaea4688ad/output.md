<div style="border:1px solid black;">

`{bm-disable-all}`

Building and searching trie using the following settings...

```
sequence: 'banana ankle baxana orange banxxa vehicle'
search_sequences: ['anana', 'banana', 'ankle']
end_marker: ¶
pad_marker: _
max_mismatch: 2
last_tallies_checkpoint_n: 3
first_indexes_checkpoint_n: 3

```


Searching `{'banana', 'anana', 'ankle'}` revealed the following was found:

 * Matched `banana` against `banana` with distance of 0 at index 0
 * Matched `anana` against `anana` with distance of 0 at index 1
 * Matched `nana a` against `banana` with distance of 2 at index 2
 * Matched `ana a` against `anana` with distance of 1 at index 3
 * Matched `a ank` against `anana` with distance of 2 at index 5
 * Matched `ankle` against `ankle` with distance of 0 at index 7
 * Matched `baxana` against `banana` with distance of 1 at index 13
 * Matched `axana` against `anana` with distance of 1 at index 14
 * Matched `ana o` against `anana` with distance of 2 at index 16
 * Matched `banxxa` against `banana` with distance of 2 at index 27
 * Matched `anxxa` against `anana` with distance of 2 at index 28
</div>

`{bm-enable-all}`

