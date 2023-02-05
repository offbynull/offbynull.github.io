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
emissions: [z,z,y]
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


The fully exploded HMM for the  ...

 * left-hand side was forward computed.
 * right-hand side was backward computed.

```{dot}
digraph G {
 graph[rankdir=LR]
 node[shape=egg, fontname="Courier-Bold", fontsize=10]
 edge[fontname="Courier-Bold", fontsize=10]
 label="ALL possible left-hand sides (forward)"
 labelloc=top
"(-1, 'SINK')" [label="(-1, 'SINK')\n0.038671885171816495"]
"(-1, 'SOURCE')" [label="(-1, 'SOURCE')\n1.0"]
"(0, 'A')" [label="(0, 'A')\n0.11401579526142158"]
"(0, 'B')" [label="(0, 'B')\n0.10151954413675898"]
"(0, 'C')" [label="(0, 'C')\n0.07095812168167187"]
"(1, 'A')" [label="(1, 'A')\n0.016771308806677928"]
"(1, 'B')" [label="(1, 'B')\n0.02882894308693349"]
"(1, 'C')" [label="(1, 'C')\n0.02015028405526415"]
"(2, 'A')" [label="(2, 'A')\n0.008939923754685136"]
"(2, 'B')" [label="(2, 'B')\n0.017500092867307002"]
"(2, 'C')" [label="(2, 'C')\n0.01223186854982436"]
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
"(2, 'A')" -> "(-1, 'SINK')"
"(2, 'B')" -> "(-1, 'SINK')"
"(2, 'B')" -> "(2, 'C')"
"(2, 'C')" -> "(-1, 'SINK')"
}
```

```{dot}
digraph G {
 graph[rankdir=LR]
 node[shape=egg, fontname="Courier-Bold", fontsize=10]
 edge[fontname="Courier-Bold", fontsize=10]
 label="ALL possible right-hand sides (backward)"
 labelloc=top
"((-1, 'SINK'), 0)" [label="((-1, 'SINK'), 0)\n1.0"]
"((-1, 'SOURCE'), 0)" [label="((-1, 'SOURCE'), 0)\n0.038671885171816495"]
"((0, 'A'), 0)" [label="((0, 'A'), 0)\n0.17995742356284505"]
"((0, 'B'), 0)" [label="((0, 'B'), 0)\n0.05697748461908122"]
"((0, 'B'), 1)" [label="((0, 'B'), 1)\n0.12184420499219953"]
"((0, 'C'), 0)" [label="((0, 'C'), 0)\n0.1743220910215963"]
"((1, 'A'), 0)" [label="((1, 'A'), 0)\n0.8300119608205517"]
"((1, 'B'), 0)" [label="((1, 'B'), 0)\n0.17939600123562208"]
"((1, 'B'), 1)" [label="((1, 'B'), 1)\n0.6791681920135297"]
"((1, 'C'), 0)" [label="((1, 'C'), 0)\n0.9716836298840401"]
"((2, 'A'), 0)" [label="((2, 'A'), 0)\n1.0"]
"((2, 'B'), 0)" [label="((2, 'B'), 0)\n1.0"]
"((2, 'B'), 1)" [label="((2, 'B'), 1)\n0.6989602079584083"]
"((2, 'C'), 0)" [label="((2, 'C'), 0)\n1.0"]
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
"((2, 'A'), 0)" -> "((-1, 'SINK'), 0)"
"((2, 'B'), 0)" -> "((-1, 'SINK'), 0)"
"((2, 'B'), 1)" -> "((2, 'C'), 0)"
"((2, 'C'), 0)" -> "((-1, 'SINK'), 0)"
}
```

The **certainty** for ['z', 'z', 'y'] when the hidden path is limited to traveling through ...

 * (0, 'A') = 0.5305660344602874
 * (0, 'B') = 0.4694339655397127
 * (0, 'C') = 0.319859455818013
 * (1, 'A') = 0.3599614253691131
 * (1, 'B') = 0.640038574630887
 * (1, 'C') = 0.506303250204181
 * (2, 'A') = 0.2311737251743916
 * (2, 'B') = 0.7688262748256085
 * (2, 'C') = 0.3162987399108944

</div>

`{bm-enable-all}`

