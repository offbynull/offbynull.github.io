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


The following isolated exploded HMM was produced -- index 1 only has the option to travel from B to A, then split based on that *edge*.

```{dot}
digraph G {
 graph[rankdir=LR]
 node[shape=egg, fontname="Courier-Bold", fontsize=10]
 edge[fontname="Courier-Bold", fontsize=10]
 label="Left-hand side"
 labelloc=top
"(-1, 'SINK')" [label="(-1, 'SINK')\n0.021937444122028846"]
"(-1, 'SOURCE')" [label="(-1, 'SOURCE')\n1.0"]
"(0, 'A')" [label="(0, 'A')\n0.29796061181645506"]
"(0, 'B')" [label="(0, 'B')\n0.28596421073677897"]
"(0, 'C')" [label="(0, 'C')\n0.19987760420524112"]
"(1, 'A')" [label="(1, 'A')\n0.11824571978144525"]
"(1, 'B')" [label="(1, 'B')\n0.2204782560617482"]
"(1, 'C')" [label="(1, 'C')\n0.1541055277072267"]
"(2, 'A')" [label="(2, 'A')\n0.025301079341836088"]
"(2, 'B')" [label="(2, 'B')\n0.04624615280665147"]
"(2, 'C')" [label="(2, 'C')\n0.03232422058301344"]
"(3, 'A')" [label="(3, 'A')\n0.00534986315041072"]
"(3, 'B')" [label="(3, 'B')\n0.009763372263762992"]
"(3, 'C')" [label="(3, 'C')\n0.0068242087078551365"]
"(-1, 'SOURCE')" -> "(0, 'A')"
"(-1, 'SOURCE')" -> "(0, 'B')"
"(0, 'A')" -> "(1, 'A')"
"(0, 'A')" -> "(1, 'B')"
"(0, 'B')" -> "(0, 'C')"
"(0, 'B')" -> "(1, 'A')"
"(0, 'C')" -> "(1, 'B')"
"(1, 'A')" -> "(2, 'A')"
"(1, 'A')" -> "(2, 'B')"
"(1, 'B')" -> "(1, 'C')"
"(1, 'B')" -> "(2, 'A')"
"(1, 'C')" -> "(2, 'B')"
"(2, 'A')" -> "(3, 'A')"
"(2, 'A')" -> "(3, 'B')"
"(2, 'B')" -> "(2, 'C')"
"(2, 'B')" -> "(3, 'A')"
"(2, 'C')" -> "(3, 'B')"
"(3, 'A')" -> "(-1, 'SINK')"
"(3, 'B')" -> "(-1, 'SINK')"
"(3, 'B')" -> "(3, 'C')"
"(3, 'C')" -> "(-1, 'SINK')"
}
```

```{dot}
digraph G {
 graph[rankdir=LR]
 node[shape=egg, fontname="Courier-Bold", fontsize=10]
 edge[fontname="Courier-Bold", fontsize=10]
 label="Right-hand side (backward)"
 labelloc=top
"((-1, 'SINK'), 0)" [label="((-1, 'SINK'), 0)\n1.0"]
"((-1, 'SOURCE'), 0)" [label="((-1, 'SOURCE'), 0)\n0.02193744412202885"]
"((0, 'A'), 0)" [label="((0, 'A'), 0)\n0.03763627156778639"]
"((0, 'B'), 0)" [label="((0, 'B'), 0)\n0.011669288290689557"]
"((0, 'B'), 1)" [label="((0, 'B'), 1)\n0.02582952175820652"]
"((0, 'C'), 0)" [label="((0, 'C'), 0)\n0.03695420921550302"]
"((1, 'A'), 0)" [label="((1, 'A'), 0)\n0.06504764994935922"]
"((1, 'B'), 0)" [label="((1, 'B'), 0)\n0.020653848703040052"]
"((1, 'B'), 1)" [label="((1, 'B'), 1)\n0.04395949770190257"]
"((1, 'C'), 0)" [label="((1, 'C'), 0)\n0.06289270433620792"]
"((2, 'A'), 0)" [label="((2, 'A'), 0)\n0.3008722054879951"]
"((2, 'B'), 0)" [label="((2, 'B'), 0)\n0.06864658258991009"]
"((2, 'B'), 1)" [label="((2, 'B'), 1)\n0.24111005033726257"]
"((2, 'C'), 0)" [label="((2, 'C'), 0)\n0.3449553316368617"]
"((3, 'A'), 0)" [label="((3, 'A'), 0)\n1.0"]
"((3, 'B'), 0)" [label="((3, 'B'), 0)\n1.0"]
"((3, 'B'), 1)" [label="((3, 'B'), 1)\n0.6989602079584083"]
"((3, 'C'), 0)" [label="((3, 'C'), 0)\n1.0"]
"((-1, 'SOURCE'), 0)" -> "((0, 'A'), 0)"
"((-1, 'SOURCE'), 0)" -> "((0, 'B'), 0)"
"((-1, 'SOURCE'), 0)" -> "((0, 'B'), 1)"
"((0, 'A'), 0)" -> "((1, 'A'), 0)"
"((0, 'A'), 0)" -> "((1, 'B'), 0)"
"((0, 'A'), 0)" -> "((1, 'B'), 1)"
"((0, 'B'), 0)" -> "((1, 'A'), 0)"
"((0, 'B'), 1)" -> "((0, 'C'), 0)"
"((0, 'C'), 0)" -> "((1, 'B'), 0)"
"((0, 'C'), 0)" -> "((1, 'B'), 1)"
"((1, 'A'), 0)" -> "((2, 'A'), 0)"
"((1, 'A'), 0)" -> "((2, 'B'), 0)"
"((1, 'A'), 0)" -> "((2, 'B'), 1)"
"((1, 'B'), 0)" -> "((2, 'A'), 0)"
"((1, 'B'), 1)" -> "((1, 'C'), 0)"
"((1, 'C'), 0)" -> "((2, 'B'), 0)"
"((1, 'C'), 0)" -> "((2, 'B'), 1)"
"((2, 'A'), 0)" -> "((3, 'A'), 0)"
"((2, 'A'), 0)" -> "((3, 'B'), 0)"
"((2, 'A'), 0)" -> "((3, 'B'), 1)"
"((2, 'B'), 0)" -> "((3, 'A'), 0)"
"((2, 'B'), 1)" -> "((2, 'C'), 0)"
"((2, 'C'), 0)" -> "((3, 'B'), 0)"
"((2, 'C'), 0)" -> "((3, 'B'), 1)"
"((3, 'A'), 0)" -> "((-1, 'SINK'), 0)"
"((3, 'B'), 0)" -> "((-1, 'SINK'), 0)"
"((3, 'B'), 1)" -> "((3, 'C'), 0)"
"((3, 'C'), 0)" -> "((-1, 'SINK'), 0)"
}
```

 * The left-hand side is computed to have 0.2204782560617482 at its sink node.
 * The middle side (the edge itself, not displayed as a graph above) is computed to 0.06864658258991009 at its sink node.
 * The right-hand side is is computed to have 0.3008722054879951 at its source node.

When the sink nodes are multiplied together, its the probability for all hidden paths that travel from B to A at index 1 of ['y', 'y', 'z', 'z']: 0.004553724543009471.

</div>

`{bm-enable-all}`

