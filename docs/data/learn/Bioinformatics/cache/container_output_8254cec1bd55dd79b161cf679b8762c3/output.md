<div style="border:1px solid black;">

`{bm-disable-all}`

Building profile and determining emission probabilities using the following settings...

```
alignment:
  - [G, -, T, -, C]
  - [-, C, T, A, -]
  - [-, T, T, A, -]
  - [-, -, T, -, C]
  - [G, -, -, -, -]
column_removal_threshold: 0.59

```

At each row of the profile, the following emissions are possible ...

 * Arriving at -1 from the I direction:
  * G=0.5
  * C=0.25
  * T=0.25
 * Arriving at 0 from the M direction:
  * T=1.0
 * Arriving at 0 from the I direction:
  * C=0.5
  * A=0.5

</div>

`{bm-enable-all}`

