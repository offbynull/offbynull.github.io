<div style="border:1px solid black;">

`{bm-disable-all}`

Given the following graph...

````{dot}
digraph {
  node [shape=plaintext]
  "D"
  "A"
  "C"
  "E"
  "B"
  "A" -> "B" [label="1.0"]
  "A" -> "C" [label="3.0"]
  "B" -> "C" [label="1.0"]
  "C" -> "D" [label="2.0"]
  "C" -> "E" [label="1.0"]
}
````

... the path with the max weight between A and E ...

 * Maximum path = A -> C -> E
 * Maximum weight = 4.0

````{dot}
digraph {
  node [shape=plaintext]
  "D" [label="D (5.0)"]
  "A" [label="A (0.0)"]
  "C" [label="C (3.0)"]
  "E" [label="E (4.0)"]
  "B" [label="B (1.0)"]
  "A" -> "B" [label="1.0", color="blue"]
  "A" -> "C" [label="3.0", color="blue"]
  "B" -> "C" [label="1.0", color="black"]
  "C" -> "D" [label="2.0", color="blue"]
  "C" -> "E" [label="1.0", color="blue"]
}
````

The edges in blue signify the incoming edge that was selected for that node.

</div>

`{bm-enable-all}`

