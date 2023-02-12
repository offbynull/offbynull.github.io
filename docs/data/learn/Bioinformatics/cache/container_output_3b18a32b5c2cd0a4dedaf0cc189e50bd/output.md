<div style="border:1px solid black;">

`{bm-disable-all}`

Building HMM and computing transition / emission probability using the following settings...

```
transition_probabilities:
  SOURCE: {A: 0.5, B: 0.5}
  A: {A: 0.377, B: 0.623}
  B: {A: 0.26, B: 0.74}
emission_probabilities:
  SOURCE: {}
  A: {x: 0.176, y: 0.596, z: 0.228}
  B: {x: 0.225, y: 0.572, z: 0.203}
transition_to_symbol_pairs: [[[SOURCE,B],z], [[B,A],z], [[A,A],z], [[A,A],y], [[A,A],x], [[A,A],y], [[A,A],y], [[A,A],z], [[A,A],z], [[A,A],x]]

```


The following HMM was produced ...

```{dot}
digraph G {
 graph[rankdir=LR]
 node[shape=egg, fontname="Courier-Bold", fontsize=10]
 edge[fontname="Courier-Bold", fontsize=10]
"STATE_A" [label="A"]
"STATE_B" [label="B"]
"STATE_SOURCE" [label="SOURCE"]
"STATE_A" -> "STATE_A" [label="0.377"]
"STATE_A" -> "STATE_B" [label="0.623"]
"STATE_B" -> "STATE_A" [label="0.26"]
"STATE_B" -> "STATE_B" [label="0.74"]
"STATE_SOURCE" -> "STATE_A" [label="0.5"]
"STATE_SOURCE" -> "STATE_B" [label="0.5"]
"SYMBOL_x" [label="x", style="dashed"]
"STATE_A" -> "SYMBOL_x" [label="0.176", style="dashed"]
"SYMBOL_y" [label="y", style="dashed"]
"STATE_A" -> "SYMBOL_y" [label="0.596", style="dashed"]
"SYMBOL_z" [label="z", style="dashed"]
"STATE_A" -> "SYMBOL_z" [label="0.228", style="dashed"]
"STATE_B" -> "SYMBOL_x" [label="0.225", style="dashed"]
"STATE_B" -> "SYMBOL_y" [label="0.572", style="dashed"]
"STATE_B" -> "SYMBOL_z" [label="0.203", style="dashed"]
}
```

Probability of traveling through and emitting [(('SOURCE', 'B'), 'z'), (('B', 'A'), 'z'), (('A', 'A'), 'z'), (('A', 'A'), 'y'), (('A', 'A'), 'x'), (('A', 'A'), 'y'), (('A', 'A'), 'y'), (('A', 'A'), 'z'), (('A', 'A'), 'z'), (('A', 'A'), 'x')] is 1.908418837511679e-10

</div>

`{bm-enable-all}`

