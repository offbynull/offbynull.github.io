<div style="border:1px solid black;">

`{bm-disable-all}`

Building Viterbi graph and finding the max product weight using the following settings...

```
transition_probabilities:
  SOURCE: {A: 0.5, B: 0.5}
  A: {A: 0.377, B: 0.623}
  B: {A: 1.0}
emission_probabilities:
  SOURCE: {}
  A: {x: 0.176, y: 0.596, z: 0.228}
  B: {x: 0.225, y: 0.572, z: 0.203}
source_state: SOURCE
sink_state: SINK  # Doesn't have to exist in HMM, but must be unique.
emissions: [z,z,x,x,y]

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
"STATE_B" -> "STATE_A" [label="1.0"]
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

The following Viterbi graph was produced for the HMM and the emitted sequence ['z', 'z', 'x', 'x', 'y'] ...

```{dot}
digraph G {
 graph[rankdir=LR]
 node[shape=egg, fontname="Courier-Bold", fontsize=10]
 edge[fontname="Courier-Bold", fontsize=10]
"(-1, 'SINK')" [label="(-1, 'SINK')"]
"(-1, 'SOURCE')" [label="(-1, 'SOURCE')"]
"(0, 'A')" [label="(0, 'A')"]
"(0, 'B')" [label="(0, 'B')"]
"(1, 'A')" [label="(1, 'A')"]
"(1, 'B')" [label="(1, 'B')"]
"(2, 'A')" [label="(2, 'A')"]
"(2, 'B')" [label="(2, 'B')"]
"(3, 'A')" [label="(3, 'A')"]
"(3, 'B')" [label="(3, 'B')"]
"(4, 'A')" [label="(4, 'A')"]
"(4, 'B')" [label="(4, 'B')"]
"(-1, 'SOURCE')" -> "(0, 'A')" [label="0.114"]
"(-1, 'SOURCE')" -> "(0, 'B')" [label="0.1015"]
"(0, 'A')" -> "(1, 'A')" [label="0.085956"]
"(0, 'A')" -> "(1, 'B')" [label="0.126469"]
"(0, 'B')" -> "(1, 'A')" [label="0.228"]
"(1, 'A')" -> "(2, 'A')" [label="0.066352"]
"(1, 'A')" -> "(2, 'B')" [label="0.140175"]
"(1, 'B')" -> "(2, 'A')" [label="0.176"]
"(2, 'A')" -> "(3, 'A')" [label="0.066352"]
"(2, 'A')" -> "(3, 'B')" [label="0.140175"]
"(2, 'B')" -> "(3, 'A')" [label="0.176"]
"(3, 'A')" -> "(4, 'A')" [label="0.224692"]
"(3, 'A')" -> "(4, 'B')" [label="0.35635599999999995"]
"(3, 'B')" -> "(4, 'A')" [label="0.596"]
"(4, 'A')" -> "(-1, 'SINK')" [label="1.0"]
"(4, 'B')" -> "(-1, 'SINK')" [label="1.0"]
}
```

The hidden path with the max product weight in this Viterbi graph is [('SOURCE', 'A'), ('A', 'B'), ('B', 'A'), ('A', 'B'), ('B', 'A'), ('A', 'SINK')] (max product weight = 0.00021199149043490877).

</div>

`{bm-enable-all}`

