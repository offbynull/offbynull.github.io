<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

Notice that the first column of the matrix is just the last column but lexicographically sorted.

When storing the first and last columns of the matrix, you technically only need to store just the elements of the last column. You can generate the first column by simply sorting the elements of the last column. For example, the elements in last column of the example above are "annb¶aa". To convert that back into the first and last columns of the matrix with symbol instance counts, the steps are as follows:

1. Last column: augment "annb¶aa" with symbol instance counts: [a1, n1, n2, b1, ¶1, a2, a3].

   In this case, the augmentation isn't with symbol counts from the original sequence ("banana¶") but from the sequence that makes up the last column ("annb¶aa").

2. First column: Sorting the result of step 1, _taking the symbol instance counts into account_: [¶1, a1, a2, a3, b1, n1, n2].

   The sort is still a lexicographical sort but the symbol instance are included as well. A lower symbol instance count should be given precedence over a higher symbol instance count. For example, once sorted, "a2" should appear before "a3" but after "a1". This is done because the ordering of symbol occurrences need to be preserved between the first and last columns.

The end result of reconstructing from "annb¶aa" is the following first and last columns, ...

```{svgbob}
+--+--+
|¶1|a1|
|a1|n1|
|a2|n2|
|a3|b1|
|b1|¶1|
|n1|a2|
|n2|a3|
+--+--+
```

While the symbol instance counts are different, the mapping between symbol instances between the first and last columns are the same, meaning that you can still use it to search for substrings in "banana¶"...

```{svgbob}
RECONSTRUCTED          ORIGINAL

   +--+--+             +--+--+
   |¶1|a1|             |¶1|a3|
   |a1|n1|             |a3|n2|
   |a2|n2|             |a2|n1|
   |a3|b1|      vs     |a1|b1|
   |b1|¶1|             |b1|¶1|
   |n1|a2|             |n2|a2|
   |n2|a3|             |n1|a1|
   +--+--+             +--+--+


"* search for substring nana using RECONSTRUCTED first and last column"

             "2 x na"                        "1 x nana"
.------------------------------.  .------------------------->*
|                              |  |                           
|  +--+--+           +--+--+   |  |  +--+--+    
|  |¶1|a1|      *<-- |¶1|a1| <-+  |  |¶1|a1|    
+- |a1|n1|           |a1|n1|   |  '- |a1|n1| <-.
'- |a2|n2|           |a2|n2|   |     |a2|n2|   |
   |a3|b1|           |a3|b1|   |     |a3|b1|   |
   |b1|¶1|           |b1|¶1|   |     |b1|¶1|   |
   |n1|a2|        .- |n1|a2| <-'     |n1|a2|   |
   |n2|a3|        |  |n2|a3|         |n2|a3|   |
   +--+--+        |  +--+--+         +--+--+   |
                  |                            |  
                  '----------------------------'  
                             "1 x nan"         
```
</div>

