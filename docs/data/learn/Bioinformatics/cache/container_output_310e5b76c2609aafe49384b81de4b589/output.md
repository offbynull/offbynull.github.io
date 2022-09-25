<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

The book describes this algorithm as the "partial suffix array" algorithm. To understand why, consider the suffix array for "banana¶" (end marker is ¶).

```{svgbob}
"SUFFIX ARRAY FOR banana"                       "SUFFIX TREE FOR banana"
                    
    0   ¶                                             banana¶   
                                             .-------------------------->*
    1   a ¶                                  |                na¶       
        |                                    |           .---------->*    
    2   a n a ¶                              |       na  | ¶              
        | | |                                |   .------>*-->*            
    3   a n a n a ¶                          | a | ¶                      
                                             +-->*-->*                    
    4   b a n a n a ¶                        | ¶                          
                                             *-->*                        
    5   n a ¶                                |   na    ¶                  
        | |                                  '------>*-->*                
    6   n a n a ¶                                    |   na¶          
                                                     '---------->*        
```

One way to think of a suffix array is that it's just a BWT matrix (symbol instance counts not included) where each row has had everything past the end marker removed. For example, consider the BWT matrix for "banana¶" vs the suffix array for "banana¶".

<table>
<tr><th>BWT</th><th>BWT (Truncated)</th><th>Suffix Array</th></tr>
<tr><td>

|   |   |   |   |   |   |   |
|---|---|---|---|---|---|---|
| ¶ | b | a | n | a | n | a |
| a | ¶ | b | a | n | a | n |
| a | n | a | ¶ | b | a | n |
| a | n | a | n | a | ¶ | b |
| b | a | n | a | n | a | ¶ |
| n | a | ¶ | b | a | n | a |
| n | a | n | a | ¶ | b | a |

</td><td>

|   |   |   |   |   |   |   |
|---|---|---|---|---|---|---|
| ¶ |   |   |   |   |   |   |
| a | ¶ |   |   |   |   |   |
| a | n | a | ¶ |   |   |   |
| a | n | a | n | a | ¶ |   |
| b | a | n | a | n | a | ¶ |
| n | a | ¶ |   |   |   |   |
| n | a | n | a | ¶ |   |   |

</td><td>

|         |
|---------|
| ¶       |
| a¶      |
| ana¶    |
| anana¶  |
| banana¶ |
| na¶     |
| nana¶   |

</td></tr>
</table>

> Why is this the case? Both BWT matrices and suffix arrays have their rows lexicographically sorted in the same way. Since each row's truncation point is always at the end marker (¶), and there's only ever a single end marker in a row, any symbols after that end marker don't effect of the lexicographic sorting of the rows.
> 
> Try it and see. Take the BWT matrix in the example above and change the symbols after the truncation point to anything other than end marker. It won't change the sort order.
> 
> |   |   |   |   |   |   |   |
> |---|---|---|---|---|---|---|
> | ¶ | z | z | z | z | z | z |
> | a | ¶ | a | a | a | a | a |
> | a | n | a | ¶ | z | z | z |
> | a | n | a | n | a | ¶ | a |
> | b | a | n | a | n | a | ¶ |
> | n | a | ¶ | z | z | z | z |
> | n | a | n | a | ¶ | a | a |

The `first_indexes` column is essentially just a suffix array. In the context of a ...

* suffix array, it's a list containing each suffix's starting index (each index is the start of a suffix in the original sequence).
* BWT matrix, it's list containing each row's starting index  (each index is the location of that row's first character in the original sequence).

This section described the BWT matrix context. For example, `first_indexes` in the table below is used to find where "ana" appears in "banana¶": [3, 1].

<table>
<tr><th>BWT Records</th><th>Search</th></tr>
<tr><td>

| first | first_indexes / suffix_offsets | last  |
|-------|--------------------------------|-------|
| (¶,1) | 6 (suffix = ¶)                 | (a,3) |
| (a,3) | 5 (suffix = a¶)                | (n,2) |
| (a,2) | 3 (suffix = ana¶)              | (n,1) |
| (a,1) | 1 (suffix = anana¶)            | (b,1) |
| (b,1) | 0 (suffix = banana¶)           | (¶,1) |
| (n,2) | 4 (suffix = na¶)               | (a,2) |
| (n,1) | 2 (suffix = nana¶)             | (a,1) |

</td><td>

```{svgbob}
"* ana occurs in banana¶ at index 3 and 1"

+--+---+--+           +--+---+--+           +--+---+--+         
|¶1| 6 |a3|     na    |¶1| 6 |a3|           |¶1| 6 |a3|
|a3| 5 |n2|-------.   |a3| 5 |n2|           |a3| 5 |n2|
|a2| 3 |n1|-----. |   |a2| 3 |n1|     .---> |a2| 3 |n1|
|a1| 1 |b1|     | |   |a1| 1 |b1|     | .-> |a1| 1 |b1|
|b1| 0 |¶1|     | |   |b1| 0 |¶1|     | |   |b1| 0 |¶1|
|n2| 4 |a2|     | '-> |n2| 4 |a2|-----' |   |n2| 4 |a2|
|n1| 2 |a1|     '---> |n1| 2 |a1|-------'   |n1| 2 |a1|
+--+---+--+           +--+---+--+    ana    +--+---+--+
```

</td></tr>
</table>

All of this leads to the following realization: The addition of `first_indexes` / `suffix_offsets` to the BWT records is pointless. The standalone suffix array algorithm can seek out these indexes on its own and the only data it needs is the original sequence and the `first_indexes` / `suffix_offsets` column (each index defines the start of a suffix in the original sequence). It doesn't need the columns `first` or `last`. What's the point of using this BWT algorithm when it needs more memory than the standalone suffix array algorithm but doesn't do anything more / better?

The situation changes a little once checkpointing comes in to play. The wider the gaps are between checkpoints, the less memory gets wasted. However, regardless of how wide the gaps are, you will never reach a point where there is no memory being wasted. It's only when the checkpointed `first_indexes` / `suffix_offsets` column is combined with a much more memory efficient BWT representation that it beats the standalone suffix array algorithm in terms of memory efficiency.

That more memory efficient BWT representation is described in a later section, which integrates checkpointed `first_indexes` / `suffix_offsets` into it: Algorithms/Single Nucleotide Polymorphism/Burrows-Wheeler Transform/Checkpointed Algorithm_TOPIC
</div>

