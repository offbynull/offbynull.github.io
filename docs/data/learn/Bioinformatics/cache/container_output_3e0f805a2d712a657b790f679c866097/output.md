<div style="border:1px solid black;">

`{bm-disable-all}`

Building profile and walking profile sequences using the following settings...

```
alignment:
  - [G, -, T, -, C]
  - [-, C, T, A, -]
  - [-, T, T, A, -]
  - [-, -, T, -, C]
  - [G, -, -, -, -]
column_removal_threshold: 0.59

```

For each sequence in the profile, this is how that sequence would be walked ...

 * Sequence in row 0:
   * Direction I (from (-1, -1) to (-1, 0))
   * Direction M (from (-1, 0) to (0, 1))
   * Direction I (from (0, 1) to (0, 2))
 * Sequence in row 1:
   * Direction I (from (-1, -1) to (-1, 0))
   * Direction M (from (-1, 0) to (0, 1))
   * Direction I (from (0, 1) to (0, 2))
 * Sequence in row 2:
   * Direction I (from (-1, -1) to (-1, 0))
   * Direction M (from (-1, 0) to (0, 1))
   * Direction I (from (0, 1) to (0, 2))
 * Sequence in row 3:
   * Direction M (from (-1, -1) to (0, 0))
   * Direction I (from (0, 0) to (0, 1))
 * Sequence in row 4:
   * Direction I (from (-1, -1) to (-1, 0))
   * Direction D (from (-1, 0) to (0, 0))

</div>

`{bm-enable-all}`

