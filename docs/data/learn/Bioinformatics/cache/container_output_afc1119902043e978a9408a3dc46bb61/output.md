<div style="border:1px solid black;">

`{bm-disable-all}`

Building Viterbi graph and finding the max product weight, after applying psuedocounts to HMM, using the following settings...

```
transition_probabilities:
  SOURCE: {A: 0.5, B: 0.5}
  A: {A: 0.377, B: 0.623}
  B: {A: 0.0,   B: 0.0}
emission_probabilities:
  SOURCE: {}
  A: {x: 0.176, y: 0.596, z: 0.228}
  B: {x: 0.0,   y: 0.572, z: 0.203}
source_state: SOURCE
sink_state: SINK  # Must not exist in HMM (used only for Viterbi graph)
emissions: [z,z,x,x,y]
pseudocount: 0.0001

```

The following HMM was produced before applying pseudocounts ...

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
"STATE_B" -> "STATE_A" [label="0.0"]
"STATE_B" -> "STATE_B" [label="0.0"]
"STATE_SOURCE" -> "STATE_A" [label="0.5"]
"STATE_SOURCE" -> "STATE_B" [label="0.5"]
"SYMBOL_x" [label="x", style="dashed"]
"STATE_A" -> "SYMBOL_x" [label="0.176", style="dashed"]
"SYMBOL_y" [label="y", style="dashed"]
"STATE_A" -> "SYMBOL_y" [label="0.596", style="dashed"]
"SYMBOL_z" [label="z", style="dashed"]
"STATE_A" -> "SYMBOL_z" [label="0.228", style="dashed"]
"STATE_B" -> "SYMBOL_x" [label="0.0", style="dashed"]
"STATE_B" -> "SYMBOL_y" [label="0.572", style="dashed"]
"STATE_B" -> "SYMBOL_z" [label="0.203", style="dashed"]
}
```

After pseudocounts are applied, the HMM becomes as follows ...

```{dot}
digraph G {
 graph[rankdir=LR]
 node[shape=egg, fontname="Courier-Bold", fontsize=10]
 edge[fontname="Courier-Bold", fontsize=10]
"STATE_A" [label="A"]
"STATE_B" [label="B"]
"STATE_SOURCE" [label="SOURCE"]
"STATE_A" -> "STATE_A" [label="0.3770245950809838"]
"STATE_A" -> "STATE_B" [label="0.6229754049190162"]
"STATE_B" -> "STATE_A" [label="0.5"]
"STATE_B" -> "STATE_B" [label="0.5"]
"STATE_SOURCE" -> "STATE_A" [label="0.5"]
"STATE_SOURCE" -> "STATE_B" [label="0.5"]
"SYMBOL_x" [label="x", style="dashed"]
"STATE_A" -> "SYMBOL_x" [label="0.17604718584424672", style="dashed"]
"SYMBOL_y" [label="y", style="dashed"]
"STATE_A" -> "SYMBOL_y" [label="0.5959212236329101", style="dashed"]
"SYMBOL_z" [label="z", style="dashed"]
"STATE_A" -> "SYMBOL_z" [label="0.22803159052284316", style="dashed"]
"STATE_B" -> "SYMBOL_x" [label="0.00012898232942086936", style="dashed"]
"STATE_B" -> "SYMBOL_y" [label="0.7379079066167935", style="dashed"]
"STATE_B" -> "SYMBOL_z" [label="0.26196311105378567", style="dashed"]
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
"(-1, 'SOURCE')" -> "(0, 'A')" [label="0.11401579526142158"]
"(-1, 'SOURCE')" -> "(0, 'B')" [label="0.13098155552689283"]
"(0, 'A')" -> "(1, 'A')" [label="0.08597351808254765"]
"(0, 'A')" -> "(1, 'B')" [label="0.16319657518257732"]
"(0, 'B')" -> "(1, 'A')" [label="0.11401579526142158"]
"(0, 'B')" -> "(1, 'B')" [label="0.13098155552689283"]
"(1, 'A')" -> "(2, 'A')" [label="0.06637411895807382"]
"(1, 'A')" -> "(2, 'B')" [label="8.035281889836401e-05"]
"(1, 'B')" -> "(2, 'A')" [label="0.08802359292212336"]
"(1, 'B')" -> "(2, 'B')" [label="6.449116471043468e-05"]
"(2, 'A')" -> "(3, 'A')" [label="0.06637411895807382"]
"(2, 'A')" -> "(3, 'B')" [label="8.035281889836401e-05"]
"(2, 'B')" -> "(3, 'A')" [label="0.08802359292212336"]
"(2, 'B')" -> "(3, 'B')" [label="6.449116471043468e-05"]
"(3, 'A')" -> "(4, 'A')" [label="0.22467695804036233"]
"(3, 'A')" -> "(4, 'B')" [label="0.4596984769175405"]
"(3, 'B')" -> "(4, 'A')" [label="0.29796061181645506"]
"(3, 'B')" -> "(4, 'B')" [label="0.36895395330839675"]
"(4, 'A')" -> "(-1, 'SINK')" [label="1.0"]
"(4, 'B')" -> "(-1, 'SINK')" [label="1.0"]
}
```

The hidden path with the max product weight in this Viterbi graph is [('SOURCE', 'A'), ('A', 'B'), ('B', 'A'), ('A', 'A'), ('A', 'B'), ('B', 'SINK')] (max product weight = 4.997433076928734e-05).

</div>

`{bm-enable-all}`

