<div style="border:1px solid black;">

`{bm-disable-all}`

Given the sequences TACT and GACGT and the score matrix...

```
INDEL=-1.0
   A  C  T  G
A  1  0  0  0
C  0  1  0  0
T  0  0  1  0
G  0  0  0  1

````

... the node weights are ...

````
   0.0  -1.0  -2.0  -3.0  -4.0
  -1.0   0.0  -1.0  -2.0  -3.0
  -2.0  -1.0   1.0   0.0  -1.0
  -3.0  -2.0   0.0   2.0   1.0
  -4.0  -3.0  -1.0   1.0   2.0
  -5.0  -3.0  -2.0   0.0   2.0
````

The sink node weight (maximum alignment path weight) is 2.0

</div>

`{bm-enable-all}`

