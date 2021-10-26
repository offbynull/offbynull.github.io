<div style="border:1px solid black;">

`{bm-disable-all}`

Given the following graph...

````{dot}
digraph {
  node [shape=plaintext]
  "E"
  "B"
  "A"
  "C"
  "D"
  "A" -> "B" [label="1.0"]
  "A" -> "C" [label="1.0"]
  "B" -> "C" [label="1.0"]
  "C" -> "D" [label="1.0"]
  "C" -> "E" [label="1.0"]
}
````

... the path with the max weight between A and E ...
 * Maximum path = A -> B -> C -> E
 * Maximum weight = 3.0
</div>

`{bm-enable-all}`

