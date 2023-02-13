<div style="border:1px solid black;">

`{bm-disable-all}`

Finding the probability of an HMM emitting a sequence, using the following settings...

```
transition_probabilities:
  SOURCE: {A: 0.5, B: 0.5}
  A: {A: 0.377, B: 0.623}
  B: {A: 0.301, C: 0.699}
  C: {B: 1.0}
emission_probabilities:
  SOURCE: {}
  A: {x: 0.176, y: 0.596, z: 0.228}
  B: {x: 0.225, y: 0.572, z: 0.203}
  C: {}
  # C set to empty dicts to identify as non-emittable hidden state.
source_state: SOURCE
sink_state: SINK
emissions: [y,y,z,z]
from_emission_idx: 1
from_hidden_state: B
to_hidden_state: A
pseudocount: 0.0001

```

The following HMM was produced AFTER applying pseudocounts ...

```{dot}
digraph G {
 graph[rankdir=LR]
 node[shape=egg, fontname="Courier-Bold", fontsize=10]
 edge[fontname="Courier-Bold", fontsize=10]
"STATE_A" [label="A"]
"STATE_B" [label="B"]
"STATE_C" [label="C"]
"STATE_SOURCE" [label="SOURCE"]
"STATE_A" -> "STATE_A" [label="0.3770245950809838"]
"STATE_A" -> "STATE_B" [label="0.6229754049190162"]
"STATE_B" -> "STATE_A" [label="0.30103979204159165"]
"STATE_B" -> "STATE_C" [label="0.6989602079584083"]
"STATE_C" -> "STATE_B" [label="1.0"]
"STATE_SOURCE" -> "STATE_A" [label="0.5"]
"STATE_SOURCE" -> "STATE_B" [label="0.5"]
"SYMBOL_x" [label="x", style="dashed"]
"STATE_A" -> "SYMBOL_x" [label="0.17604718584424672", style="dashed"]
"SYMBOL_y" [label="y", style="dashed"]
"STATE_A" -> "SYMBOL_y" [label="0.5959212236329101", style="dashed"]
"SYMBOL_z" [label="z", style="dashed"]
"STATE_A" -> "SYMBOL_z" [label="0.22803159052284316", style="dashed"]
"STATE_B" -> "SYMBOL_x" [label="0.22503249025292413", style="dashed"]
"STATE_B" -> "SYMBOL_y" [label="0.5719284214735579", style="dashed"]
"STATE_B" -> "SYMBOL_z" [label="0.20303908827351796", style="dashed"]
}
```


The following isolated exploded HMM was produced -- index 1 only has the option to travel from B to A, then split based on that node.

```{dot}
digraph G {
 graph[rankdir=LR]
 node[shape=egg, fontname="Courier-Bold", fontsize=10]
 edge[fontname="Courier-Bold", fontsize=10]
 label="Left-hand side"
 labelloc=top
"(-1, 'SOURCE')" [label="(-1, 'SOURCE')\n1.0"]
"(0, 'A')" [label="(0, 'A')\n0.29796061181645506"]
"(0, 'B')" [label="(0, 'B')\n0.28596421073677897"]
"(0, 'C')" [label="(0, 'C')\n0.19987760420524112"]
"(1, 'B')" [label="(1, 'B')\n0.2204782560617482"]
"(-1, 'SOURCE')" -> "(0, 'A')"
"(-1, 'SOURCE')" -> "(0, 'B')"
"(0, 'A')" -> "(1, 'B')"
"(0, 'B')" -> "(0, 'C')"
"(0, 'C')" -> "(1, 'B')"
}
```

```{dot}
digraph G {
 graph[rankdir=LR]
 node[shape=egg, fontname="Courier-Bold", fontsize=10]
 edge[fontname="Courier-Bold", fontsize=10]
 label="Right-hand side"
 labelloc=top
"(-1, 'SINK')" [label="(-1, 'SINK')\n0.020653848703040056"]
"(1, 'B')" [label="(1, 'B')\n1.0"]
"(2, 'A')" [label="(2, 'A')\n0.06864658258991009"]
"(3, 'A')" [label="(3, 'A')\n0.005901788209598736"]
"(3, 'B')" [label="(3, 'B')\n0.008682993530006478"]
"(3, 'C')" [label="(3, 'C')\n0.006069066963434841"]
"(1, 'B')" -> "(2, 'A')"
"(2, 'A')" -> "(3, 'A')"
"(2, 'A')" -> "(3, 'B')"
"(3, 'A')" -> "(-1, 'SINK')"
"(3, 'B')" -> "(-1, 'SINK')"
"(3, 'B')" -> "(3, 'C')"
"(3, 'C')" -> "(-1, 'SINK')"
}
```

 * The left-hand side is computed to have 0.2204782560617482 at its sink node.
 * The right-hand side is is computed to have 0.020653848703040056 at its sink node.

When the sink nodes are multiplied together, its the probability for all hidden paths that travel from B to A at index 1 of ['y', 'y', 'z', 'z']: 0.004553724543009471.

</div>

`{bm-enable-all}`

