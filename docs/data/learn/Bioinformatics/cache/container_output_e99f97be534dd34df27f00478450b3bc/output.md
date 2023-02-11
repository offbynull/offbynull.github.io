<div style="border:1px solid black;">

`{bm-disable-all}`

Generate a backwards graph of an HMM emitting a sequence, using the following settings...

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

```

The following HMM was produced ...

```{dot}
digraph G {
 graph[rankdir=LR]
 node[shape=egg, fontname="Courier-Bold", fontsize=10]
 edge[fontname="Courier-Bold", fontsize=10]
"STATE_A" [label="A"]
"STATE_B" [label="B"]
"STATE_C" [label="C"]
"STATE_SOURCE" [label="SOURCE"]
"STATE_A" -> "STATE_A" [label="0.377"]
"STATE_A" -> "STATE_B" [label="0.623"]
"STATE_B" -> "STATE_A" [label="0.301"]
"STATE_B" -> "STATE_C" [label="0.699"]
"STATE_C" -> "STATE_B" [label="1.0"]
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

The following forward exploded HMM was produced for the HMM and the emitted sequence ['z', 'z', 'y'] ...

```{dot}
digraph G {
 graph[rankdir=LR]
 node[shape=egg, fontname="Courier-Bold", fontsize=10]
 edge[fontname="Courier-Bold", fontsize=10]
 label="Forward graph"
 labelloc=top
"(-1, 'SINK')" [label="(-1, 'SINK')"]
"(-1, 'SOURCE')" [label="(-1, 'SOURCE')"]
"(0, 'A')" [label="(0, 'A')"]
"(0, 'B')" [label="(0, 'B')"]
"(0, 'C')" [label="(0, 'C')"]
"(1, 'A')" [label="(1, 'A')"]
"(1, 'B')" [label="(1, 'B')"]
"(1, 'C')" [label="(1, 'C')"]
"(2, 'A')" [label="(2, 'A')"]
"(2, 'B')" [label="(2, 'B')"]
"(2, 'C')" [label="(2, 'C')"]
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

The following backward exploded HMM was produced for the HMM and the emitted sequence ['z', 'z', 'y'] ...

```{dot}
digraph G {
 graph[rankdir=LR]
 node[shape=egg, fontname="Courier-Bold", fontsize=10]
 edge[fontname="Courier-Bold", fontsize=10]
 label="Backward graph"
 labelloc=top
"((-1, 'SINK'), 0)" [label="((-1, 'SINK'), 0)"]
"((-1, 'SOURCE'), 0)" [label="((-1, 'SOURCE'), 0)"]
"((0, 'A'), 0)" [label="((0, 'A'), 0)"]
"((0, 'B'), 0)" [label="((0, 'B'), 0)"]
"((0, 'B'), 1)" [label="((0, 'B'), 1)"]
"((0, 'C'), 0)" [label="((0, 'C'), 0)"]
"((1, 'A'), 0)" [label="((1, 'A'), 0)"]
"((1, 'B'), 0)" [label="((1, 'B'), 0)"]
"((1, 'B'), 1)" [label="((1, 'B'), 1)"]
"((1, 'C'), 0)" [label="((1, 'C'), 0)"]
"((2, 'A'), 0)" [label="((2, 'A'), 0)"]
"((2, 'B'), 0)" [label="((2, 'B'), 0)"]
"((2, 'B'), 1)" [label="((2, 'B'), 1)"]
"((2, 'C'), 0)" [label="((2, 'C'), 0)"]
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

</div>

`{bm-enable-all}`

